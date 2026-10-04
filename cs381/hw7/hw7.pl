/* course(course_number, course_name, credits) */

course(cs101,python, 2).
course(mth210, calculusI, 5).
course(cs120, web_design, 3).
course(cs200, data_structures, 4).
course(cs210, algorithms, 4).
course(wrt101, basic_writing, 3).

/* section(CRN, course_number) */

section(1522,cs101).
section(1122,cs101).
section(2322,mth210).
section(2421,cs120).
section(8522,mth210).
section(1621,cs200).
section(7822,mth210).
section(2822,cs210).
section(3522,wrt101).

/* place( CRN, building, time) */

place(1522,owen102,10).
place(1122,dear118,11).
place(2322,with210,11).
place(2421,cov216,15).
place(8522,kec1001,13).
place(1621,cov216,14).
place(7822,kec1001,14).
place(2822,owen102,13).
place(3522,with210,15).

/* enroll(sid, CRN) */

enroll(122,1522).
enroll(122,8522).
enroll(150,1522).
enroll(150,2421).
enroll(212,7822).
enroll(300,2822).
enroll(300,8522).
enroll(310,3522).
enroll(310,8522).
enroll(310,1621).
enroll(175,2822).
enroll(175,7822).
enroll(175,3522).
enroll(410,1621).
enroll(410,7822).
enroll(113,3522).

/* student(sid, student_name, major) */

student(122, mary, cs).
student(150, john, math).
student(212, jim, ece).
student(300, lee, cs).
student(310, pat, cs).
student(175, amy, math).
student(410, john, cs).
student(113, zoe, ece).

% schedule/4
schedule(Sid, Course_name, Building, Time) :- 
    enroll(Sid, CRN),
    place(CRN, Building, Time),
    section(CRN, Course_number),
    course(Course_number, Course_name, _).

% schedule/3
schedule(Sid, Student_name, Course_name) :-
    enroll(Sid, CRN),
    student(Sid, Student_name, _),
    section(CRN, Course_number),
    course(Course_number, Course_name, _).

% offer/4
offer(Course_number, Course_name, CRN, Time) :-
    course(Course_number, Course_name, _),
    section(CRN, Course_number),
    place(CRN, _, Time).

% conflict/3
conflict(Sid, CRN1, CRN2) :-
    enroll(Sid, CRN1),
    place(CRN1, _, T),
    enroll(Sid, CRN2),
    place(CRN2, _, T),
    CRN1 \= CRN2.

% meet/2
meet(SID1, SID2) :-
    enroll(SID1, CRN1),
    enroll(SID2, CRN2),
    SID1 \= SID2,
    place(CRN1, Building, T1),
    place(CRN2, Building, T2),
    T2 - T1 < 2,
    T1 - T2 < 2.

% roster/2
roster(CRN, Student_name) :- 
    enroll(SID, CRN),
    student(SID, Student_name, _).

% highCredits/1
highCredits(Course_name) :-
    course(_, Course_name, Credits),
    Credits > 3.

% rdup/2
rdup([],[]).
rdup([H, H|T], L) :- rdup([H|T], L), !.
rdup([H|T], [H|L]) :- rdup(T, L).

% flat/2
flat([], []).
flat([H|T], [H|L]) :-
    not(is_list(H)),
    flat(T, L).
flat([H|T], L) :-
    is_list(H),
    flat(H, FH),
    flat(T, FT),
    append(FH, FT, L).

% project/3
project([], _, []).
project([I|Arr], L, [Ele|Result]) :- 
    nth1(I, L, Ele),
    project(Arr, L, Result).
