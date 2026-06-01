user_input = input("Enter your test marks (0 to 100): ")
marks = float(user_input)

if marks < 0 or marks > 100:
    print("Error: Please enter a valid mark between 0 and 100.")
elif marks >= 90:
    print("Result: Pass | Grade: A")
elif marks >= 80:
    print("Result: Pass | Grade: B")
elif marks >= 70:
    print("Result: Pass | Grade: C")
elif marks >= 50:
    print("Result: Pass | Grade: D")
else:
    print("Result: Fail | Grade: F")
