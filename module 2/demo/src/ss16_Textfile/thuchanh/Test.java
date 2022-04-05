package ss16_Textfile.thuchanh;
import java.util.ArrayList;
import java.util.List;

public class Test {
    public static void main(String[] args) {
        FileUtils fileUtils = new FileUtils();
////        fileUtils.writeToFile("data1.txt");
//        System.out.println("Write file success");
////        fileUtils.readFromFile("data1.txt");
//        fileUtils.readFileByBufferReader("data1.txt");
//        List<Student> students = new ArrayList<>();
//        students.add(new Student("STU001", "Hoai An", 18));
//        students.add(new Student("STU002", "Thang", 19));
//        students.add(new Student("STU003", "Hieu", 20));
//        students.add(new Student("STU004", "Hung", 18));
//        students.add(new Student("STU005", "Nam", 20));
//        fileUtils.writeListStudent("student.csv", students);

        List<Student> studentList = fileUtils.readStudentFromFile("student.csv");
        studentList.forEach(System.out::println);
    }
}