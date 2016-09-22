package DocumentClassification

import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.classification.{LogisticRegression, OneVsRest}
import org.apache.spark.ml.feature.{HashingTF, StringIndexer, Tokenizer}
import org.apache.spark.sql.SQLContext
import org.apache.spark.{SparkConf, SparkContext}

import TextUtilities.TextCleaner.cleanText
import TextUtilities.TextTools.lemmatizeText

object ModelArchitecture {

  def preProcessText(txt: String): String = {
    var text = cleanText(txt)
    if (text.length > 0) text = lemmatizeText(text).toString
    text
  }

  def main(args: Array[String]) {
    val conf = new SparkConf().setMaster("local[*]").setAppName("CorpusCleaner")
    val sc = new SparkContext(conf)
    val sqlContext = new SQLContext(sc)

    val tweets_path = "data/sample_data.txt"
    val tweetsRDD = sc.textFile(tweets_path).map(x => {
      val row = x.split("#")
      (row(0),preProcessText(row(1)))
    })

//    tweetsRDD.foreach(println)

    val trainingDF = sqlContext.createDataFrame(tweetsRDD).toDF("category", "cleaned_text")
    val Array(trainingData, testData) = trainingDF.randomSplit(Array(0.7, 0.3))
    trainingData.show()
//
//
//    // Model Architecture
    val indexer = new StringIndexer().setInputCol("category").setOutputCol("label")
    val tokenizer = new Tokenizer().setInputCol("cleaned_text").setOutputCol("tokens")
    val hashingTF = new HashingTF().setInputCol("tokens").setOutputCol("features").setNumFeatures(20)
    val lr = new LogisticRegression().setMaxIter(100).setRegParam(0.001)
    val ovr = new OneVsRest().setClassifier(lr)
//
    val pipeline = new Pipeline().setStages(Array(indexer, tokenizer, hashingTF, ovr))
    val model = pipeline.fit(trainingData)


// Testing Data
val testing = "data/test.txt"
    val testRDD = sc.textFile(testing).map(x => {
      val row = x.split("#")
      (1,preProcessText(row(1)))
    })

    val testingDF = sqlContext.createDataFrame(testRDD).toDF("id","cleaned_text")


    val prediction = model.transform(testData).select("cleaned_text","category","prediction")
    prediction.foreach(println)
  }
}
