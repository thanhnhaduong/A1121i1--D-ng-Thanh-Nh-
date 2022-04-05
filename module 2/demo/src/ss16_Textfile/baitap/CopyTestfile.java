package ss16_Textfile.baitap;

import ss16_Textfile.thuchanh.ReadAndWriteFile;
import ss16_Textfile.thuchanh.ReadFileExample;


import java.util.List;
import java.util.Scanner;

public class CopyTestfile {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Nhập đường dẫn file đọc: ");
        String path = scanner.nextLine();
        System.out.println("Nhập đường dẫn file ghi: ");
        String path1 = scanner.nextLine();
        ReadFileExample readfileEx = new ReadFileExample();
        readfileEx.readFileText(path);

        ReadAndWriteFile readAndWriteFile = new ReadAndWriteFile();
        readAndWriteFile.writeFile(path1);


    }
}
