package TextUtilities

import edu.stanford.nlp.simple.Sentence
import scala.collection.mutable.ListBuffer

object TextTools {

  def lemmatizeText(txt: String) = new Sentence(txt).lemmas().toArray().mkString(" ")

//  def lemmatizeWord(txt: String) = new Sentence(txt).lemmas().toArray().mkString(" ")

  def getPOSTagsText(txt: String): String = {
    val sent = new Sentence(txt)
    val tags = sent.posTags().toArray()
    val words = sent.words().toArray()
    var pos_tags = new ListBuffer[String]
    for ((wrd,i) <- words.view.zipWithIndex) pos_tags += wrd.toString+"|"+tags(i).toString
    pos_tags.mkString(",")
  }

//  def getPOSTagWord(txt: String): String = {
//    val sent = new Sentence(txt)
//    val tags = sent.posTags().toArray()
//    val words = sent.words().toArray()
//    var pos_tags = new ListBuffer[String]
//    for ((wrd,i) <- words.view.zipWithIndex) pos_tags += wrd.toString+"|"+tags(i).toString
//    pos_tags.mkString(",")
//  }



//  def main(args: Array[String]) {
//    val txt = "running runner runs youngest younger higher highest"
//    println(posTagging(txt))
//  }

}
