package executors;

import babelnet.WikiPageMapping;
import clusters.Clusters;
import clusters.ClustersMeter;
import constants.DatasetName;
import it.uniroma1.lcl.babelnet.data.BabelCategory;
import twittermodel.BabelCategoryModel;
import twittermodel.BabelDomainModel;
import twittermodel.Dataset;

import io.Cache;
import io.Utils;
import twittermodel.WikiPageModel;
import utils.Chrono;

import java.util.Collection;
import java.util.HashSet;
import java.util.Set;


@Deprecated
public class ReadingPhaseExecutor {

    public static void main(String[] args) throws Utils.CacheNotPresent {

//        for (DatasetName name : DatasetName.values()) {
//           Chrono c = new Chrono("Reading... " + name);
//
////            Dataset d = DatasetReader.readDataset(name, Dimension.COMPLETE);
////            Cache.write(name, d);
//
////            Dataset d = Cache.DatasetCache.read(name, Dimension.SMALL);
//            c.millis();
//        }
        //

        Dataset d = Cache.DatasetCache.read(DatasetName.WIKIMID);
        System.out.println(d.getWikiPages().get(0));

        Collection<WikiPageModel> set = d.getWikiPages().values();
        System.out.println(set.size());
        System.out.println(new HashSet<>(set).size());

        Collection<BabelCategoryModel> s2 = d.getBabelCategories().values();
        System.out.println(s2.size());
        System.out.println(new HashSet<>(s2).size());

        Collection<BabelDomainModel> s3 = d.getBabelDomains().values();
        System.out.println(s3.size());
        System.out.println(new HashSet<>(s3).size());
//        Clusters c = Cache.ClustersWikiMidCache.readCategories();
//        System.out.println(c.report(d, "BNCAT:EN:Swedish_DJs", 10));
////
////        System.out.println(
////        );
////        System.out.println(c.getCluster("37962832"));
//        WikiPageMapping w = Cache.WikiMappingCache.read();
////        System.out.println(w.clustersStats());
//        //
////        System.out.println(c.clusterInspection(d, "BNCAT:EN:Swedish_people_of_Italian_descent"));
//
//        ClustersMeter cm = new ClustersMeter(d, c, w.getPagesToCategories());
//
//        Chrono cr = new Chrono();
//        System.out.println(cm.clustersJaccardSimilarity("BNCAT:EN:Musical_groups_from_Detroit,_Michigan", "BNCAT:EN:Musical_groups_from_Detroit,_Michigan"));
//        System.out.println(cm.clustersJaccardSimilarity("BNCAT:EN:Musical_groups_from_Detroit,_Michigan", "BNCAT:EN:Song_recordings_produced_by_Muff_Winwood"));
//        System.out.println(cm.clustersJaccardSimilarity("BNCAT:EN:English_pop_music_groups", "BNCAT:EN:People_from_Mableton,_Georgia"));
//        System.out.println(cm.clustersJaccardSimilarity("BNCAT:EN:Living_people", "BNCAT:EN:People_from_Mableton,_Georgia"));
//        cr.millis();
//        WikiPageMapping d = WikiPageMapping.getInstance();
//        Clusters clu = new ClusterGenerator(d, w).loadCategoryClusters();
//        clu.clustersStats(d, "")
//        System.out.println(clu.clustersStats(d, "BNCAT:EN:Films_directed_by_Tony_Kaye_(director)"));
//        System.out.println(d);
//        System.out.println(w.clustersStats(200));
//        System.out.println(d.clustersStats(200));

//        d = Cache.WikiMappingCache.read(Dimension.COMPLETE);
//        System.out.println(d);
//        System.out.println(d.clustersStats());
    }
}
