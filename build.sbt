name := "WoltersKluver"
version := "1.0"
scalaVersion := "2.11.8"

ivyScala := ivyScala.value map { _.copy(overrideScalaVersion = true) }
resolvers += Resolver.sonatypeRepo("public")
resolvers += "bintray-spark-packages" at "https://dl.bintray.com/spark-packages/maven/"

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % "1.6.2",
  "org.apache.spark" %% "spark-sql" % "1.6.2",
  "org.apache.spark" %% "spark-mllib" % "1.6.2"
)

libraryDependencies += "com.google.protobuf" % "protobuf-java" % "2.6.1"

unmanagedJars in Compile += file("lib/stanford-corenlp.jar")
unmanagedJars in Compile += file("lib/stanford-corenlp-models.jar")