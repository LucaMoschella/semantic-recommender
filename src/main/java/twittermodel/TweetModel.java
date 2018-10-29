package twittermodel;

import java.util.HashMap;
import java.util.Map;

/**
 * Models a "tweet"
 */
public class TweetModel extends ObjectModel {

    /**
     * The authorId of the tweet.
     * If this object if associated to an user, this field is written.
     */
    private int authorId;

    /**
     * The interested this tweet is talking about
     */
    private int interestId;

    /**
     * The source from which the interestId has been found
     */
    private String interestUrl;

    public TweetModel(String id) {
        super(id);
    }

    public void setAuthorId(UserModel authorId) {
        assert authorId != null;

        this.authorId = authorId.getId();
    }

    public void setInterestUrl(String interestSource) {
        assert interestSource != null && !interestSource.equals("");

        this.interestUrl = interestSource;
    }

    public void setInterestId(InterestModel interestId) {
        assert interestId != null;

        this.interestId = interestId.getId();
    }

    public int getAuthorId() {
        assert authorId >= 0;

        return authorId;
    }

    public String getInterestUrl() {
        assert interestUrl != null;

        return interestUrl;
    }

    public int getInterestId() {
        assert interestId >= 0;

        return interestId;
    }

    public InterestModel getInterestModel(Map<Integer, InterestModel> interests) {
        assert interests.containsKey(getInterestId());

        InterestModel interest = interests.get(getInterestId());
        assert interest.getId() == getInterestId();

        return interest;
    }

    public WikiPageModel getWikiPageModel(Map<Integer, InterestModel> interests, Map<Integer, WikiPageModel> pages) {
        return getInterestModel(interests).getWikiPageModel(pages);
    }

    @Override
    public String toString(){
        return String.format("(tweet: %d {interestId: %s, interestUrl: %s})", getId(), interestId, interestUrl);
    }
}
