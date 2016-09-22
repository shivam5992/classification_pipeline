package TextUtilities

import TextTools.getPOSTagsText

object TextProcess {


  def getPosTagsDistributions(corpus: List[String]): Unit ={
    corpus.foreach(line => {
      println(line)
//      getPOSTagsText(line).foreach(x => {
//        println(x)
//      })
    })

  }

  def getBigramDistributions(): Unit ={

  }

}
