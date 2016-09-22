//package Regression
//
//import org.apache.spark.ml.Pipeline
//import org.apache.spark.ml.classification.RandomForestClassifier
//import org.apache.spark.ml.feature.{IndexToString, StringIndexer, VectorAssembler}
//import org.apache.spark.sql.SQLContext
//import org.apache.spark.sql.types._
//import org.apache.spark.{SparkConf, SparkContext}
//import org.apache.spark.sql.functions._
//
//object binaryClassification {
//
//  def main(args: Array[String]) {
//    val conf = new SparkConf().setMaster("local[*]").setAppName("Regeression")
//    val sc = new SparkContext(conf)
//    val sqlContext = new SQLContext(sc)
//
//    val schemaArray = Array(StructField("PassengerId", IntegerType, nullable = true),
//                            StructField("Survived", IntegerType, nullable = true),
//                            StructField("Pclass", IntegerType, nullable = true),
//                            StructField("Name", StringType, nullable = true),
//                            StructField("Sex", StringType, nullable = true),
//                            StructField("Age", FloatType, nullable = true),
//                            StructField("SibSp", IntegerType, nullable = true),
//                            StructField("Parch", IntegerType, nullable = true),
//                            StructField("Ticket", StringType, nullable = true),
//                            StructField("Fare", FloatType, nullable = true),
//                            StructField("Cabin", StringType, nullable = true),
//                            StructField("Embarked", StringType, nullable = true)
//                          )
//    val trainSchema = StructType(schemaArray)
//    val testSchema = StructType(schemaArray.filter(p => p.name != "Survived"))
//
//    val train_path = "/media/inno/01D04251141467101/WKData/classification/train.csv"
//    val test_path = "/media/inno/01D04251141467101/WKData/classification/test.csv"
//
//    val trainDF = sqlContext.read
//                            .format("org.databricks.spark.csv")
//                            .option("header","true")
//                            .schema(trainSchema)
//                            .load(train_path)
//    val testDF = sqlContext.read
//                            .format("org.databricks.spark.csv")
//                            .option("header","true")
//                            .schema(trainSchema)
//                            .load(test_path)
//
//
//    // Feature Engineering
//    // Derive Title fron name, create family size -
//    // uniariate analysis, bivariate analysis, multicolinearity
//    // missing values , outliers
////    val avgAge = trainDF.select(avg("Age"))
////    println(avgAge)
////    val avgFare = 1
////    val trainDFWithValues = trainDF.na.fill(Map("Fare" -> avgFare, "Age" -> avgAge, "Embarked" -> "S"))
//    val categoricalFeatColNames = Seq("Pclass", "Sex", "Embarked")
//    val stringIndexers = categoricalFeatColNames.map { colName =>
//      new StringIndexer()
//        .setInputCol(colName)
//        .setOutputCol(colName + "Indexed")
//        .fit(trainDF)
//    }
//
//    val labelIndexer = new StringIndexer()
//      .setInputCol("Survived")
//      .setOutputCol("SurvivedIndexed")
//      .fit(trainDF)
//
//    val numericFeatColNames = Seq("Age", "SibSp", "Parch", "Fare")
//    val idxdCategoricalFeatColName = categoricalFeatColNames.map(_ + "Indexed")
//    val allIdxdFeatColNames = numericFeatColNames ++ idxdCategoricalFeatColName
//    val assembler = new VectorAssembler()
//      .setInputCols(Array(allIdxdFeatColNames: _*))
//      .setOutputCol("Features")
//
//
//    val randomForest = new RandomForestClassifier()
//      .setLabelCol("SurvivedIndexed")
//      .setFeaturesCol("Features")
//
//
//    val labelConverter = new IndexToString()
//      .setInputCol("prediction")
//      .setOutputCol("predictedLabel")
//      .setLabels(labelIndexer.labels)
//
//    val pipeline = new Pipeline().setStages(Array.concat(
//      stringIndexers.toArray,
//      Array(labelIndexer, assembler, randomForest, labelConverter)
//    ))
//
//  }
//}