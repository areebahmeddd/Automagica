import java.util.concurrent.TimeUnit;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.By;

class Instagram {
    public static void main(String[] args) {
        System.setProperty("webdriver.chrome.driver", "path\\to\\chromedriver.exe");

        WebDriver browser = new ChromeDriver();
        browser.manage().window().maximize();
        browser.get("https://www.instagram.com/accounts/login/");
        browser.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);

        WebElement username = browser.findElement(By.name("username")).sendKeys("USERNAME");
        WebElement password = browser.findElement(By.name("password")).sendKeys("PASSWORD");
        WebElement login = browser.findElement(By.xpath("//button[@type='submit']")).click();
    }
}