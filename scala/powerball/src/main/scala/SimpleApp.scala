import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._

import net.ruippeixotog.scalascraper.browser.JsoupBrowser

//val browser = JsoupBrowser()
//val doc = browser.parseFile("src/test/resources/example.html")
//val doc2 = browser.get("http://example.com")

object SimpleApp {
  def main(args: Array[String]) {
    val browser = JsoupBrowser()
    val doc = browser.get("https://www.lottery.net/powerball/numbers/2020")
    for { headline <- doc >?> element("h1 a")
      } println(headline.text)

  }
}
