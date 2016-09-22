package DocumentClassification

import org.apache.spark.{SparkConf, SparkContext}
import TextUtilities.TextCleaner.cleanText
import TextUtilities.TextTools.lemmatizeText
import TextUtilities.TextProcess.getPosTagsDistributions

object EDA {

  def main(args: Array[String]) {
    val tweets_path = "/media/inno/01D04251141467101/WKData/tweets/disney.txt"
    val lines = scala.io.Source.fromFile(tweets_path).getLines().map(x => x.split("@@")(1))

    lines.foreach(row => {
      var sent = cleanText(row)
      sent = lemmatizeText(sent)
//      val postag_distribution = getPosTagsDistributions(sent)
//      println(lemma)
    })
  }
}
