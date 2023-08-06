(untitleoop) a package for beginning Python OOP
===============================================

โปรแกรมนี้ใช้ำหรับเริ่มต้นเขียนโปรแกรมแบบ Object Oriented Program

วิธีติดตั้ง
~~~~~~~~~~~

เปิด CMD / Terminal

.. code:: python

   pip install untitloop

วิธีใช้
~~~~~~~

-  เปิด IDLE ขึ้นมาแล้วพิมพ์…

.. code:: python

   from untitleoop import Student,Tesla,SpecialStudent,Teacher
   # Day 0
   print('\n--- Day 0 ---')
   allstudent = []

   teacher1 = Teacher(fullname='Ada Lovelace')
   teacher2 = Teacher(fullname='Billy Gloves')
   print(teacher1.students)


   # Day 1
   print('\n--- Day 1 ---')
   st1 = Student('Alberto','Einsteino')
   allstudent.append(st1)
   teacher2.AddStudent(st1)  
   print(st1.fullname)

   # Day 2
   print('\n--- Day 2 ---')
   st2 = Student('Steven','Joops')
   allstudent.append(st2)
   teacher2.AddStudent(st2)
   print(st2.fullname)

   # Day 3
   print('\n--- Day 3 ---')
   for i in range(3):
       st1.Coding()
   st2.Coding()
   st1.showExp()
   st2.showExp()

   # Day 4
   print('\n--- Day 4 ---')
   stp1 = SpecialStudent('Helmut','Schmeicer','Zemo')
   allstudent.append(stp1)
   teacher1.AddStudent(stp1)
   print(stp1.fullname)
   print('Professor give me 20 points')
   stp1.exp = 20
   stp1.Coding()
   stp1.showExp()

   # Day 5
   print('\n--- Day 5 ---')
   print('How do you go home?')
   print('{}, {} and {}'.format(allstudent[0],allstudent[1],allstudent[2]))
   for st in allstudent:
       print('I\'m {}, going by {}'.format(st.name,st.vehicle))
       if isinstance(st,SpecialStudent):
           st.vehicle.SelfDriving(st)

   # Day 6
   print('\n--- Day 6 ---')
   teacher1.CheckStudents()
   teacher2.CheckStudents()

   print('Total exp for 2 guys is ',st1 + st2)

พัฒนาโดย: ByllyVylly
