from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query
#create the web application
webapp = Flask(__name__)

#provide a route where requests on the web application can be addressed
# @webapp.route('/hello')
# #provide a view (fancy name for a function) which responds to any requests on this route
# def hello():
#     return "Hello World!"

# # @webapp.route('/')

# # def home():
# #     return 'home page'
# @webapp.route('/browse_bsg_people')
# #the name of this function is just a cosmetic thing
# def browse_people():
#     print("Fetching and rendering people web page")
#     db_connection = connect_to_database()
#     query = "SELECT fname, lname, homeworld, age, id from bsg_people;"
#     result = execute_query(db_connection, query).fetchall()
#     print(result)
#     return render_template('people_browse.html', rows=result)

# @webapp.route('/add_new_people', methods=['POST','GET'])
# def add_new_people():
#     db_connection = connect_to_database()
#     if request.method == 'GET':
#         query = 'SELECT id, name from bsg_planets'
#         result = execute_query(db_connection, query).fetchall()
#         print(result)

#         return render_template('people_add_new.html', planets = result)
#     elif request.method == 'POST':
#         print("Add new people!")
#         fname = request.form['fname']
#         lname = request.form['lname']
#         age = request.form['age']
#         homeworld = request.form['homeworld']

#         query = 'INSERT INTO bsg_people (fname, lname, age, homeworld) VALUES (%s,%s,%s,%s)'
#         data = (fname, lname, age, homeworld)
#         execute_query(db_connection, query, data)
#         return ('Person added!')
@webapp.route('/teachers')
def teachers_view():
    # return "<p>Are you looking for /db_test or /hello or <a href='/browse_bsg_people'>/browse_bsg_people</a> or /add_new_people or /update_people/id or /delete_people/id </p>"
    db_connection = connect_to_database()
    query = "SELECT * from Teachers;"
    result = execute_query(db_connection, query).fetchall()
  

    teach_results = []
    print(result)
    for i in range(0, len(result)):
        
        query2 = "SELECT * from TeacherClassList where teacher_id = %s;"
        data = (result[i][0],)
        result2 = execute_query(db_connection, query2, data).fetchall()
       
        classes = []
        for j in range(0, len(result2)):
            
            query3 = "SELECT * from Classes WHERE class_id = %s;"
            data = (result2[j][2],)
            class_result = execute_query(db_connection, query3, data).fetchall()
        
            classes.append(class_result)
    
        teacher = (result[i], classes)
       
        teach_results.append(teacher)
       
    
    return render_template('teachers.html', rows=teach_results)
@webapp.route('/update_teacher/<int:id>', methods=['POST','GET'])
def update_teacher(id):
    db_connection = connect_to_database()

    if request.method == 'GET':
        query = 'SELECT * from Teachers WHERE teacher_id = %s;' % (id)
        result = execute_query(db_connection, query).fetchall()
        print(result[0][0], 'this is result')
        return render_template('update_teacher.html', teach=result)
    elif request.method == 'POST':
        # print(request.form)
        first_name = request.form['first_name']
        last_name = request.form['lname']
       
        query = "UPDATE Teachers SET first_name = %s , last_name = %s WHERE teacher_id = %s; " 
        data = (first_name, last_name, id)
        execute_query(db_connection, query, data)

        return redirect('/teachers')
@webapp.route('/add_teacher', methods=['POST','GET'])
def add_teacher():
    db_connection = connect_to_database()

    if request.method == 'GET':
        query = 'SELECT id, name from bsg_planets'
        result = execute_query(db_connection, query).fetchall()
        print(result)
    elif request.method == 'POST':
        # print(request.form)
        first_name = request.form['first_name']
        last_name = request.form['lname']
        query = "INSERT INTO Teachers (first_name, last_name) VALUES (%s,%s);"
        data = (first_name, last_name)
        execute_query(db_connection, query, data)
       
        return redirect('/teachers')
@webapp.route('/delete_teacher/<int:id>')
def delete_teacher(id):
    '''deletes a teacher with the given id'''
    db_connection = connect_to_database()
    query1 = "DELETE from TeacherClassList where teacher_id = %s;"
    data = (id,)
    execute_query(db_connection, query1, data)
    query = "DELETE from Teachers where teacher_id = %s;"
    data = (id,)

    result = execute_query(db_connection, query, data)
    return redirect('/teachers')
# Grades
@webapp.route('/update_grade/<int:id>', methods=['POST','GET'])
def update_grade(id):
    db_connection = connect_to_database()

    if request.method == 'GET':
        query = 'SELECT * from Grades WHERE grade_id = %s;' 
        data = (id,)
        result = execute_query(db_connection, query, data).fetchall()
        print(result, 'grade result edit')
        return render_template('update_grade.html', grade=result)
    elif request.method == 'POST':
        print(request.form)
        # first_name = request.form['first_name']
        # last_name = request.form['lname']
        grade_number = request.form['grade_number']
        # print(grade_number)
        query = "UPDATE Grades SET grade_number = %s  WHERE grade_id = %s; " 
        data = (grade_number, id)
        # data = (first_name, last_name, id)
        execute_query(db_connection, query, data)

        return redirect('/grades')
@webapp.route('/add_grade/<int:id>/<int:class_id>', methods=['POST','GET'])
def add_grade(id, class_id):
    db_connection = connect_to_database()

    if request.method == 'GET':
        
        query1 = "SELECT * from Students where student_id = %s;"
        data = (id,)
        student_result = execute_query(db_connection, query1, data).fetchall()
        # print(student_result, 'student_result')

        query2 = "SELECT * from Classes where class_id = %s;"
        data = (class_id,)
        class_result = execute_query(db_connection, query2, data).fetchall()
        result = student_result, class_result
        # print(result[1][0][1], 'result 0')
        # print(class_result, 'class_result')
        return render_template('add_grade.html', rows=result)
    elif request.method == 'POST':
        print(request.form, 'request')
        grade_number = request.form['grade']
        query3 = "INSERT INTO Grades (grade_number, class_id) VALUES (%s, %s); "
        data = (grade_number, class_id)
        execute_query(db_connection, query3, data)
        query4 = "SELECT LAST_INSERT_ID() LIMIT 1;"
        grade_id = execute_query(db_connection, query4).fetchall()
        # print(grade_id[0][0], 'grade id')
        query5 = "INSERT INTO StudentGradeList (grade_id, student_id) VALUES(%s, %s);"
        data = (grade_id[0][0], id)
        execute_query(db_connection, query5, data)
        return redirect('/grades')
@webapp.route('/delete_grade/<int:id>')

def delete_grade(id):
    # print(id)
    db_connection = connect_to_database()
    query = "DELETE from StudentGradeList where grade_id = %s;"
    data = (id,)
    execute_query(db_connection, query, data)
    query = "DELETE from Grades where grade_id = %s;"
    data = (id,)

    result = execute_query(db_connection, query, data)
    return redirect('/grades')
@webapp.route('/grades')
def grades_view():
    # return "<p>Are you looking for /db_test or /hello or <a href='/browse_bsg_people'>/browse_bsg_people</a> or /add_new_people or /update_people/id or /delete_people/id </p>"
    db_connection = connect_to_database()
    query = "SELECT * from Grades;"
    result = execute_query(db_connection, query).fetchall()
    query2 = "SELECT * from Students;"
    result2 = execute_query(db_connection, query2).fetchall()
    grades_res = (result, result2)

    student_list = []
    query = "SELECT * from StudentGradeList;"
    result3 = execute_query(db_connection, query).fetchall()
    for res in result3:
        query = "SELECT * from Students where student_id = %s;"
        data = (res[2],)
        student = execute_query(db_connection, query, data).fetchall()

        query = "SELECT * from Grades where grade_id = %s;"
        data = (res[1],)
        grade = execute_query(db_connection, query, data).fetchall()

        query = "SELECT * from Classes where class_id = %s;"
        data = (grade[0][2],)
        class_n = execute_query(db_connection, query, data).fetchall()
        final = student, grade, class_n
        student_list.append(final)
    for g in student_list:
        print(g[1])
    # print(result3)

    # print(grades_res)
   
  
    return render_template('grades.html', grade_result = student_list)
@webapp.route('/delete_student/<int:id>')
def delete_student(id):
    '''deletes a student with the given id'''
    db_connection = connect_to_database()
    query1 = "DELETE from StudentList where student_id = %s;"
    data = (id,)
    result1 = execute_query(db_connection, query1, data)
    query6 = "DELETE from StudentGradeList where student_id = %s;"
    execute_query(db_connection, query6, data)
    query2 = "DELETE from Students where student_id = %s;"
    result2 = execute_query(db_connection, query2, data)
    
    # print('hello')
   
    return redirect('/students')
@webapp.route('/update_student/<int:id>', methods=['POST','GET'])
def update_student(id):
    db_connection = connect_to_database()

    if request.method == 'GET':
        query = "SELECT * from Students where student_id = %s;"
        data = (id,)
        student_result = execute_query(db_connection, query, data).fetchall()

        query2 = "SELECT * from StudentList where student_id = %s;"
        class_result = execute_query(db_connection, query2, data).fetchall()

        
        class_list = []
        for i in range(0, len(class_result)):
            class_list.append(class_result[i][1])
        # print(class_list)
        current_classes = []
        for j in range (0, len(class_list)):
            query = "SELECT * from Classes where class_id = %s;"
            data = (class_list[j],)
            class_name = execute_query(db_connection, query, data).fetchall()
            current_classes.append(class_name)
        # print(current_classes)
        query4 = "SELECT * from Classes;"
        not_enrolled = execute_query(db_connection, query4).fetchall()
        # print(not_enrolled)

        not_enroll = []
        for class_en in not_enrolled:
            # print(class_en, 'class en')
            if class_list.count(class_en[0]) == 0:
                not_enroll.append(class_en)
        # print(not_enroll)
        student = student_result, current_classes, not_enroll
        # print(student[1])
        # print(student, current_classes, 'curr')
        # print(student[1][0])
        # print(student[0], 'student')
        # print(not_enroll, 'not enroll')
        # print(class_list)
        # print(class_result)

        return render_template('update_student.html', student=student)
    elif request.method == 'POST':
        print(request.form, 'form')
        first_name = request.form['first_name']
        last_name = request.form['lname']
        drop_list = request.form.getlist('drop')
        new_enroll = request.form.getlist('new_enroll')

        query = "UPDATE Students SET first_name = %s, last_name = %s where student_id = %s;"
        data = (first_name, last_name, id)
        execute_query(db_connection, query, data)
        
        for i in range(0, len(drop_list)):
           
            
            query3 = "SELECT * from StudentGradeList where student_id = %s; "
            data = (id,)

            result = execute_query(db_connection, query3, data).fetchall()
            
            grades_final = []

            for res in result:
                
                query4 = "SELECT * from Grades where grade_id = %s; "
                data = (res[1],)
                grade = execute_query(db_connection, query4, data).fetchall()
                if grade:
                    
                    if grade[0][2] == int(drop_list[i]):
                       
                        grades_final.append(grade)
            
            for grade in grades_final:
                query = "DELETE from StudentGradeList where grade_id = %s;"
                data = (grade[0][0],)
                execute_query(db_connection, query, data)
                query = "DELETE from Grades where grade_id = %s;"
                data = (grade[0][0],)
                execute_query(db_connection, query, data)
            
            query2 = "DELETE from StudentList where student_id = %s and class_student_id = %s;"
            data = (id, drop_list[i])
            execute_query(db_connection, query2, data)
            # print(result, 'result')
            # print(drop_list[i], 'droplist')

        # print(drop_list, new_enroll)
        # first_name = request.form['first_name']
        # last_name = request.form['lname']
        
        # query = "UPDATE Teachers SET first_name = %s , last_name = %s WHERE teacher_id = %s " 
        # data = (first_name, last_name, id)
        # execute_query(db_connection, query, data)

        return redirect('/students')
@webapp.route('/add_student', methods=['POST','GET'])
def add_student():
    db_connection = connect_to_database()

    if request.method == 'GET':
        query = 'SELECT id, name from bsg_planets'
        result = execute_query(db_connection, query).fetchall()
        print(result)
    elif request.method == 'POST':
        
        print(request.form.getlist('classes'))

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        classes = request.form.getlist('classes')

        query = "INSERT INTO Students (first_name, last_name) VALUES (%s, %s);"
        data = (first_name, last_name)
        execute_query(db_connection, query, data)

        query2 = "SELECT LAST_INSERT_ID() LIMIT 1;"
        student_id = execute_query(db_connection, query2).fetchall()
        print(student_id[0][0])
        for i in range(0, len(classes)):
            
            query3 = "INSERT INTO StudentList (class_student_id, student_id) VALUES (%s, %s);"
            data = (classes[i], student_id[0][0])
            execute_query(db_connection, query3, data)
        # name = request.form['title']
        # teacher_id = request.form['teacher']
    
        # query = "INSERT INTO Classes (name) VALUES (%s);"
        # data = (name,)
        # execute_query(db_connection, query, data)
        # query2 = "SELECT LAST_INSERT_ID() LIMIT 1;"
        # class_id = execute_query(db_connection, query2).fetchall()
        # class_id = class_id[0][0]
        # teacher_class_list_id = teacher_id
      
        # query3 = "INSERT INTO TeacherClassList (teacher_class_list_id, class_id) VALUES (%s, %s);"
        # data = (teacher_class_list_id, class_id)
        # execute_query(db_connection, query3, data)
     
        
        return redirect('/students')
@webapp.route('/student_search' ,methods=['POST','GET'])
def student_search():
    db_connection = connect_to_database()
    if request.method == 'GET':
        # query = 'SELECT id, name from bsg_planets'
        # result = execute_query(db_connection, query).fetchall()
        # print(result)
        return redirect('/students')
    elif request.method == 'POST':
        print(request.form, 'search form')
        first_name = request.form['first_name']

        query = "SELECT * from Students where first_name = %s;"
        data = (first_name,)
        students_result = execute_query(db_connection, query, data).fetchall()
        # print(students_result)
        return render_template('search_results.html', students = students_result)
@webapp.route('/students')
def students_view():
    # return "<p>Are you looking for /db_test or /hello or <a href='/browse_bsg_people'>/browse_bsg_people</a> or /add_new_people or /update_people/id or /delete_people/id </p>"
    db_connection = connect_to_database()
    query = "SELECT * from Students;"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    query2 = "SELECT * from Classes;"
    result2 = execute_query(db_connection, query2).fetchall()

    student_list = []
    for i in range(0, len(result)):

        class_list = []
        class_ids = []
        query4 = "SELECT * from StudentList where student_id = %s;"
        data = (result[i][0],)
        result4 = execute_query(db_connection, query4, data).fetchall()
        for j in range(0, len(result4)):
            query5 = "SELECT * from Classes where class_id = %s;"
            data = (result4[j][1],)
            result5 = execute_query(db_connection, query5, data).fetchall()
            query6 = "SELECT * from StudentGradeList where student_id = %s;"
            data = (result[i][0],)
            result6 = execute_query(db_connection, query6, data).fetchall()
            

            print(result6, 'result6')
            if len(result6) > 0:
                for r in result6:
                    # print(r, 'r')
                    query = "SELECT * from Grades where grade_id = %s and class_id = %s;"
                    data = (r[1], result4[j][1])
                    grade_number = execute_query(db_connection, query, data).fetchall()
                    # print(grade_number, 'grade #')
                    if grade_number:
                        # print(grade_number[0])
                        # print(class_list, 'class_list')
                        # print(class_ids, grade_number , 'test')
                        if class_ids.count(result4[j][1]) == 1:
                            for x in range(0, len(class_list)):
                                if class_list[x][0][0] == result4[j][1]:
                                    

                                    class_list.remove(class_list[x])
                                    
                                    class_res = result5[0], grade_number[0][1]
                                    class_list.append(class_res)
            
                            # print(class_list, 'class_list')
                        else:
                            class_res = result5[0], grade_number[0][1]
                            class_list.append(class_res)
                            class_ids.append(result4[j][1])
                    else:
                        if class_ids.count(result4[j][1]) == 0:
                            class_res = result5[0], ()
                            class_list.append(class_res)
                            class_ids.append(result4[j][1])
                        # for c in class_list:
                        #     print(c, 'class_list')
                        #     class_res = result5[0], result6
                        #     class_list.append(class_res)
            else:
                # print(class_list, 'class_list')
                class_res = result5[0], result6
                class_list.append(class_res)
                class_ids.append(result4[j][1])
        # print('hit')
        # print(class_list)
        student = result[i], class_list
        # print(student, 'student')
        student_list.append(student)
    # print(student_list, 'student_list')
    result = student_list, result2
    # print(result)
    return render_template('students.html', rows=result)

@webapp.route('/delete_class/<int:id>')
def delete_class(id):
    '''deletes a class with the given id'''
    db_connection = connect_to_database()
    query1 = "DELETE from TeacherClassList where class_id = %s;"
    data = (id,)
    result1 = execute_query(db_connection, query1, data)
    query2 = "DELETE from StudentList where class_student_id = %s;"
    result2 = execute_query(db_connection, query2, data)
    query3 = "SELECT * from Grades where class_id = %s;"
    grade_result = execute_query(db_connection, query3, data).fetchall()

    # print(grade_result)
    if len(grade_result) > 0:
        query4 = "DELETE from StudentGradeList where grade_id = %s; "
        data = (grade_result[0][0])
        execute_query(db_connection, query4, data)
        query5 = "DELETE from Grades where grade_id = %s;"
        execute_query(db_connection, query5, data)

    
    # print(grade_result)
    query = "DELETE from Classes where class_id = %s;"
    data = (id,)
    result = execute_query(db_connection, query, data)
   
    return redirect('/classes')
@webapp.route('/add_class', methods=['POST','GET'])
def add_class():
    db_connection = connect_to_database()

    if request.method == 'GET':
        query = 'SELECT id, name from bsg_planets'
        result = execute_query(db_connection, query).fetchall()
        print(result)
    elif request.method == 'POST':
        print(request.form)
        name = request.form['title']
        teacher_id = request.form['teacher']
    
        query = "INSERT INTO Classes (name) VALUES (%s);"
        data = (name,)
        execute_query(db_connection, query, data)
        query2 = "SELECT LAST_INSERT_ID() LIMIT 1;"
        class_id = execute_query(db_connection, query2).fetchall()
        class_id = class_id[0][0]
        teacher_class_list_id = teacher_id
      
        query3 = "INSERT INTO TeacherClassList (teacher_id, class_id) VALUES (%s, %s);"
        data = (teacher_class_list_id, class_id)
        execute_query(db_connection, query3, data)
     
        
        return redirect('/classes')
@webapp.route('/update_class/<int:id>', methods=['POST','GET'])
def update_class(id):
    db_connection = connect_to_database()

    if request.method == 'GET':
        query = 'SELECT * from Classes WHERE class_id = %s;' % (id)
        result = execute_query(db_connection, query).fetchall()

        query2 = "SELECT * from Teachers;"
        result2 = execute_query(db_connection, query2).fetchall()
        result = (result, result2)
     
        return render_template('update_class.html', result=result)
    elif request.method == 'POST':
        print(request.form, 'post')
        name = request.form['class_name']
        teacher_class_list_id = request.form['teacher']
     
        query = "DELETE from TeacherClassList where class_id = %s;"
        data = (id,)
        execute_query(db_connection, query, data)
        query2 = "UPDATE Classes SET name = %s WHERE class_id = %s;"
        data = (name, id,)
        execute_query(db_connection, query2, data)
        query3 = "INSERT INTO TeacherClassList (teacher_id, class_id) VALUES (%s, %s);"
        data = (teacher_class_list_id, id,)
        execute_query(db_connection, query3, data)
       
        

        return redirect('/classes')
@webapp.route('/classes')
def classes_view():
    # return "<p>Are you looking for /db_test or /hello or <a href='/browse_bsg_people'>/browse_bsg_people</a> or /add_new_people or /update_people/id or /delete_people/id </p>"
    db_connection = connect_to_database()
    query = "SELECT * from Classes;"
    result = execute_query(db_connection, query).fetchall()
    query2 = "SELECT * from Teachers;"
    teach_result = execute_query(db_connection, query2).fetchall()
    
    final_results = []
    # print(result, 'result')
    for i in range(0, len(result)):
      
        query3 = "SELECT * from TeacherClassList WHERE class_id = %s;"
        data = (result[i][0],)
        result2 = execute_query(db_connection, query3, data).fetchall()

        # print(result2[0], 'result2')
        query5 = "SELECT * from StudentList WHERE class_student_id = %s;"
        result5 = execute_query(db_connection, query5, data).fetchall()
        
        student_list = []
        for j in range(0, len(result5)):
            query6 = "SELECT * from Students where student_id = %s;"
            data = (result5[j][2],)
            student = execute_query(db_connection, query6, data).fetchall()
            student_list.append(student[0])
       
        if len(result2) > 0:
            query4 = "SELECT * from Teachers WHERE teacher_id = %s;"
            data = (result2[0][1],)
            result3 = execute_query(db_connection, query4, data).fetchall()
            
            join_result = (result[i][0], result[i][1], result3[0][0], result3[0][1], result3[0][2])

            join_result = join_result, student_list
            # print(join_result, 'join result')
            final_results.append(join_result)
        
    final_results = (final_results, teach_result)
    
    # for c in final_results[0]:
    #     print(c, 'c')
    # print(final_results[0], 'results 0')
    return render_template('classes.html', result = final_results)
@webapp.route('/')
def index():
    # return "<p>Are you looking for /db_test or /hello or <a href='/browse_bsg_people'>/browse_bsg_people</a> or /add_new_people or /update_people/id or /delete_people/id </p>"
    return render_template('index.html')


# @webapp.route('/home')
# def home():
#     db_connection = connect_to_database()
#     query = "DROP TABLE IF EXISTS diagnostic;"
#     execute_query(db_connection, query)
#     query = "CREATE TABLE diagnostic(id INT PRIMARY KEY, text VARCHAR(255) NOT NULL);"
#     execute_query(db_connection, query)
#     query = "INSERT INTO diagnostic (text) VALUES ('MySQL is working');"
#     execute_query(db_connection, query)
#     query = "SELECT * from diagnostic;"
#     result = execute_query(db_connection, query)
#     for r in result:
#         print(f"{r[0]}, {r[1]}")
#     return render_template('home.html', result = result)

# @webapp.route('/db_test')
# def test_database_connection():
#     print("Executing a sample query on the database using the credentials from db_credentials.py")
#     db_connection = connect_to_database()
#     query = "SELECT * from bsg_people;"
#     result = execute_query(db_connection, query)
#     return render_template('db_test.html', rows=result)

# #display update form and process any updates, using the same function
# @webapp.route('/update_people/<int:id>', methods=['POST','GET'])
# def update_people(id):
#     print('In the function')
#     db_connection = connect_to_database()
#     #display existing data
#     if request.method == 'GET':
#         print('The GET request')
#         people_query = 'SELECT id, fname, lname, homeworld, age from bsg_people WHERE id = %s'  % (id)
#         people_result = execute_query(db_connection, people_query).fetchone()

#         if people_result == None:
#             return "No such person found!"

#         planets_query = 'SELECT id, name from bsg_planets'
#         planets_results = execute_query(db_connection, planets_query).fetchall()

#         print('Returning')
#         return render_template('people_update.html', planets = planets_results, person = people_result)
#     elif request.method == 'POST':
#         print('The POST request')
#         character_id = request.form['character_id']
#         fname = request.form['fname']
#         lname = request.form['lname']
#         age = request.form['age']
#         homeworld = request.form['homeworld']

#         query = "UPDATE bsg_people SET fname = %s, lname = %s, age = %s, homeworld = %s WHERE id = %s"
#         data = (fname, lname, age, homeworld, character_id)
#         result = execute_query(db_connection, query, data)
#         print(str(result.rowcount) + " row(s) updated")

#         return redirect('/browse_bsg_people')

# @webapp.route('/delete_people/<int:id>')
# def delete_people(id):
#     '''deletes a person with the given id'''
#     db_connection = connect_to_database()
#     query = "DELETE FROM bsg_people WHERE id = %s"
#     data = (id,)

#     result = execute_query(db_connection, query, data)
#     return (str(result.rowcount) + "row deleted")