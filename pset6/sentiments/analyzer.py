import nltk
from nltk.tokenize import TweetTokenizer

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        
        # create a set for positive words and load from file.
        self.pwords = set()
        
        filep = open(positives, "r")
        for line in filep:
            if line.startswith( ';' ) is False:
                self.pwords.add(line.rstrip("\n"))
        filep.close()
        
        # create a set for negative words and load from file.
        self.nwords = set()
        
        filen = open(negatives, "r")
        for line in filen:
            if line.startswith( ';' ) is False:
                self.nwords.add(line.rstrip("\n"))
        filen.close()        

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        
        # tokenize input text
        token = TweetTokenizer(strip_handles=True)
        L = token.tokenize(text)
        
        senti = 0
        
        # build sentiment score
        for i in L:
            # check if word is in negative word set
            if i.lower() in self.nwords:
                senti = senti - 1
            # check if word is in positive word set
            elif i.lower() in self.pwords:
                senti = senti + 1
        # return calculated sentiment
        return senti
