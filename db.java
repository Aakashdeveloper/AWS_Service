import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;
import java.sql.ResultSet;
import java.sql.PreparedStatement;


public class ProductComponent {

    public void printProductList(double lowPrice, double highPrice) throws Exception {

        try (Connection connection =
                     DriverManager.getConnection("jdbc:mysql://database-1.c83fdlzp5lmg.us-east-2.rds.amazonaws.com:3306/classicmodels?"
                             + "user=admin&password=admin987&serverTimezone=UTC");

             PreparedStatement preparedStatement = connection
                     .prepareStatement("SELECT * FROM products "
                             + "WHERE buyPrice BETWEEN ? AND ?");) {

            preparedStatement.setDouble(1, lowPrice);
            preparedStatement.setDouble(2, highPrice);



            try (ResultSet resultSet = preparedStatement.executeQuery();) {

                while (resultSet.next()) {

                    String name = resultSet.getString("productName");
                    System.out.println(name);
                }

            }
        }
    }

}