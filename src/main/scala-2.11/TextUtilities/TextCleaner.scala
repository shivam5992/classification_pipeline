package TextUtilities

/**
  * Created by Shivam Bansal on 7/1/16.
  * */

import java.io.PrintWriter

import scala.collection.mutable.ListBuffer
import scala.io.Source

object TextCleaner {
  var metaRegex = Map[String, String]()

  metaRegex += ("punctuation" -> "[^a-zA-Z0-9]")
  metaRegex += ("digits" -> "\\b\\d+\\b")
  metaRegex += ("alphanumerics" -> "(\\b[0-9]+[a-zA-Z]+\\b)|(\\b+[a-zA-Z]+[0-9]+\\b)|(\\b[a-zA-Z]+[0-9]+[a-zA-Z]+\\b)")
  metaRegex += ("white_space" -> "\\s+")
  metaRegex += ("small_words" -> "\\b[a-zA-Z0-9]{1,2}\\b")
  metaRegex += ("urls" -> "(https?\\://)\\S+")
  //  expressionRegex, mentionsRegex, hashtagsRegex

  var metaStopwords = Map[String, List[String]]()
  metaStopwords += ("english" -> Source.fromFile("src/main/resources/stopwords.txt").getLines().toList )
  //  locationsStopWords, personStopWords


  def removeRegex(txt: String, flag: String): String = {
    val regex = metaRegex.get(flag)
    var cleaned = txt
    regex match {
      case Some(value) =>
        if (value.equals("white_space")) cleaned = txt.replaceAll(value, "")
        else cleaned = txt.replaceAll(value, " ")
      case None => println("No regex flag matched")
    }
    cleaned
  }



  def removeCustomWords(txt: String, flag: String): String ={
    var words = txt.split(" ")
    val stopwords = metaStopwords.get(flag)
    stopwords match {
      case Some(value) => words = words.filter(x => !value.contains(x))
      case None => println("No stopword flag matched")
    }
    words.mkString(" ")
  }



  def lookupValues(txt: String, lookupMap: Map[String, String]): String ={
    val words = txt.split(" ")
    var reformed = new ListBuffer[String]
    words.foreach(x => {
      if (lookupMap.contains(x)){
        val value = lookupMap.get(x)
        value match {
          case Some(dt) => reformed += dt
          case None => println("Not matched")
        }
      }
      else reformed += x
    })
    reformed.toString().mkString(" ")
  }


  def cleanText(txt: String) : String = {
    var text = txt.toLowerCase
    text = removeRegex(text,"urls")
    text = removeRegex(text,"punctuation")
    text = removeRegex(text,"digits")
    text = removeRegex(text,"small_words")
    text = removeRegex(text,"alphanumerics")
    text = removeRegex(text,"white_space")
    text = removeCustomWords(text, "english")
    text
  }

  def cleanDocuments(input_path: String, output_path: String): Unit = {
    val documents = new java.io.File(input_path).listFiles.filter(_.getName.endsWith(".html"))
    documents.foreach( x => {
      val txt = Source.fromFile(x).mkString
      val cleaned = cleanText(txt)
      val fname = x.toString.replace(input_path,"")
      new PrintWriter(output_path+fname) { write(cleaned); close }
    })
  }


//  def main(args: Array[String]) {
//    val string = "how hello http://sdf.com"
//    println(removeCustomWords(string,"english"))
//  }

}