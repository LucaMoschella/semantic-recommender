import scipy.sparse
# import hdbscan

import utils
from constants import *
from chronometer import Chrono
# from sklearn.cluster import *
from java_export import JavaExport
from config import Config


class Clusterizator:

    TWEET_CATDOM_IMPORTANCE = 0.20
    PERSONAL_PAGE_IMPORTANCE = 0.20
    LIKED_ITEMS_CATDOM_IMPORTANCE = 0.50

    #  #users x #cat
    def sparse_user2tweetcat(self, data):
        chrono = Chrono("Computing user2tweet matrix...")
        T = scipy.sparse.lil_matrix((self.num_users, self.num_cat))
        for u in data.user2tweet_catdom_counter:
            for c in data.user2tweet_catdom_counter[u]:
                u_index = self.users2index[u]
                c_index = self.categories2index[c]
                T[u_index, c_index] = data.user2tweet_catdom_counter[u][c]

        T = T * Clusterizator.TWEET_CATDOM_IMPORTANCE
        chrono.millis()

        del data.user2tweet_catdom_counter
        # return T.tocsr()
        return T

    #  #users x #cat

    def sparse_user2personalcat(self, data):
        chrono = Chrono("Computing user2personal matrix...")
        P = scipy.sparse.lil_matrix((self.num_users, self.num_cat))
        for u in data.user2personalPage_catdom:
            for c in data.user2personalPage_catdom[u]:
                u_index = self.users2index[u]
                c_index = self.categories2index[c]
                P[u_index, c_index] = 1

        P = P * Clusterizator.PERSONAL_PAGE_IMPORTANCE
        chrono.millis()

        del data.user2personalPage_catdom
        # return P.tocsr()
        return P

    #  #users x #cat

    def sparse_user2likedcat(self, data):
        chrono = Chrono("Computing user2likedcat matrix...")
        L = scipy.sparse.lil_matrix((self.num_users, self.num_cat))
        for u in data.user2likedItems_wikipage:
            for page in data.user2likeItems_wikipage[u]:
                for c in data.pages2catdom[page]:
                    u_index = self.users2index[u]
                    c_index = self.categories2index[c]
                    L[u_index, c_index] += 1

        L = L * Clusterizator.LIKED_ITEMS_CATDOM_IMPORTANCE
        chrono.millis()

        del data.user2likedItems_wikipage
        # return L.tocsr()
        return L

    def sparse_user2followout(self, data):
        chrono = Chrono("Computing followOut matrix...")
        F = scipy.sparse.lil_matrix((self.num_users, self.num_users))
        for u in data.user2followOut:
            for f in data.user2followOut[u]:
                u_index = self.users2index[u]
                f_index = self.users2index[f]
                F[u_index, f_index] = 1
        chrono.millis()

        del data.user2followOut
        # return F.tocsr()
        return F

    #  minore di 1, esponente non deve essere negativo
    FOLLOW_OUT_CATDOM_IMPORTANCE = 0.10
    MAX_USER_DISTANCE = 3

    def compute_matrix(self, data):
        chrono1 = Chrono("Computing M....")
        T = self.sparse_user2tweetcat(data)
        P = self.sparse_user2personalcat(data)
        L = self.sparse_user2likedcat(data)

        F = self.sparse_user2followout(data)
        del data

        M = scipy.sparse.csr_matrix((self.num_users, self.num_cat))

        chrono3 = Chrono("Performing M + T")
        M += T
        chrono3.millis()

        chrono3 = Chrono("Performing M + P")
        M += P
        chrono3.millis()

        chrono3 = Chrono("Performing M + L")
        M += L
        chrono3.millis()

        for i in range(1, Clusterizator.MAX_USER_DISTANCE):
            chrono2 = Chrono("Computing {} power..".format(i))

            chorno4 = Chrono("Computing F @ F...")
            F @= F
            F = (F > 0).astype(float)
            # F = F.tolil()
            F.setdiag(0)
            # F = F.tocsr()
            chorno4.millis()

            for num_iter, matrix in enumerate([T, P, L]):
                chrono3 = Chrono("Computing F^i @ matrix{}".format(num_iter))
                coeff = Clusterizator.FOLLOW_OUT_CATDOM_IMPORTANCE ** i
                M += (coeff * (F @ matrix))
                chrono3.millis()

            chrono2.millis()
        chrono1.millis()
        del T, P, L, F
        return M

    def _get_opp_diagonal_matrix(self, F_i):
        D = scipy.sparse.lil_matrix((self.num_users, self.num_users))
        for i, v in enumerate(F_i.diagonal()):
            D[i, i] = -v
        return D.tocsr()

    def compute_matrix_cached(self, dataset_name, data):
        i = Config.get_instance()
        path = MatrixPath.get_path(
            dataset_name, i.cluster_over(), i.dimension(), Clusterizator.MAX_USER_DISTANCE)

        c = Chrono("Loading provider...")
        cache = None

        cache = utils.load_pickle(path)
        M = cache if cache else self.compute_matrix(data)

        if not cache:
            c.millis("generated")
            utils.save_pickle(M, path, override=True)
        else:
            c.millis("cached")

        return M

    # Data in the json export json:
    #
    # self.all_users
    # self.all_pages
    # self.all_catdom
    # self.pages2catdom
    # self.user2personalPage_catdom
    # self.user2likedItems_wikipage
    # self.user2followOut
    # self.user2tweet_catdom_counter

    def __init__(self, dataset_name):
        c = Chrono("Inizializing clusterizator...")
        obj = JavaExport.read(dataset_name)

        c2 = Chrono("Computing indexes...")
        self.categories = obj.all_catdom
        self.categories2index = {c: i for i, c in enumerate(self.categories)}
        self.num_cat = len(self.categories)

        self.pages = obj.all_pages
        self.pages2index = {p: i for i, p in enumerate(self.pages)}
        self.num_pages = len(self.pages)

        self.users = obj.all_users
        self.users2index = {u: i for i, u in enumerate(self.users)}
        self.num_users = len(self.users)
        c2.millis()

        M = self.compute_matrix_cached(dataset_name, obj)
        # P = self.sparse_user2personalcat(obj)
        # print("SOMAA: ", P.sum())
        # P = self.sparse_user2likedcat(obj)
        # print("SOMAA: ", P.sum())
        del obj
        c.millis()

    # def clusterize(self, k=1000):
    #     c = Chrono("Generate sparse matrix...")
    #     D = self.gen_sparse_matrix()
    #     c.millis()

    #     c = Chrono("Clusterize...")
    #     clusterer = hdbscan.HDBSCAN(
    #         min_cluster_size=100, algorithm='boruvka_kdtree')
    #     clusterer.fit(D.tocsr())
    #     c.millis()

    #     for (row, label) in enumerate(clusterer.labels_):
    #         print("row {} has label {}".format(row, label))


if __name__ == "__main__":
    # c = scipy.sparse.lil_matrix((5, 5))
    # c[1, 1] = 5
    # c[0, 4] = 23
    # d = scipy.sparse.lil_matrix((5, 5))
    # d[1, 1] = 5
    # d[0, 4] = 23
    # d[2, 4] = -23

    # # print("normale\n\n", d.todense())
    # # d.setdiag(0)
    # # print("diag a 0\n\n", d.todense())
    # # d = d.power(5)
    # # print("potenza\n\n", d.todense())
    # # d = (d > 0).astype(float)
    # # print("logical\n\n", d.todense())

    # c = c * 5
    # print()
    # print(c.todense())
    # print()
    # print(d.todense())
    # print()
    # print(c @ d.todense())
    Clusterizator(Dataset.WIKIMID())
