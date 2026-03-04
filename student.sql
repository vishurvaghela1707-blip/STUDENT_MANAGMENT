CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    gender VARCHAR(10),
    email VARCHAR(100) UNIQUE);
		INSERT INTO students ( id,name, age, gender, email)
		VALUES ( '1','Rahul', 20, 'Male', 'rahul@gmail.com');