package ss16_Textfile.thuchanh;

    public class Student {
        public String id;
        public String name;
        public int age;

        public Student(){}

        public Student(String id, String name, int age) {
            this.id = id;
            this.name = name;
            this.age = age;
        }

        @Override
        public String toString() {
            return "Student{" +
                    "id='" + id + '\'' +
                    ", name='" + name + '\'' +
                    ", age=" + age +
                    '}';
        }

        @Override
        public boolean equals(Object o) {
            if (o instanceof Student) {
                Student st = (Student) o;
                return this.id.equals(st.id);
            }
            return false;
        }

        @Override
        public int hashCode() {
            return 0;
        }
    }

