package ss16_Textfile.thuchanh;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class FileUtils {
    final String SEPARATION = ";";

    public void writeToFile(String path) {
        try {
            // xóa file trước khi ghi
//            FileWriter writer = new FileWriter(path);
            // ghi tiếp vào file có sẵn
            FileWriter writer = new FileWriter(path, true);
            writer.write("Hello world\nXin chao");
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void readFromFile(String path) {
        try {
            FileReader reader = new FileReader(path);
            int character = -1;
            while ((character = reader.read()) != -1) {
                System.out.print((char)character);
            }
            reader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void readFileByBufferReader(String path) {
        try {
            BufferedReader bufferedReader = new BufferedReader(new FileReader(path));
            String line = null;
            while ((line = bufferedReader.readLine()) != null) {
                System.out.println(line);
            }
            bufferedReader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void writeListStudent(String path, List<Student> students) {
        // txt, csv, tsv

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(path))) {
            writer.write("ID" + SEPARATION + "NAME" + SEPARATION + "AGE");
            for (Student student: students) {
                writer.newLine();
                writer.write(student.id + SEPARATION + student.name
                        + SEPARATION + student.age);
                writer.flush();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public List<Student> readStudentFromFile(String path) {
        List<Student> students = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(path))){
            String line = null;
            // bỏ qua header
            line = reader.readLine();
            while ((line = reader.readLine()) != null) {
                String[] values = line.split(SEPARATION);
                String id = values[0];
                String name = values[1];
                int age = Integer.parseInt(values[2]);
                students.add(new Student(id, name, age));
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        return students;
    }
}