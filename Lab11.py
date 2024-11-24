import os
import matplotlib.pyplot as plt



def read_students():
    students = {}
    with open("data/students.txt", "r") as file:
        for line in file:
            line = line.strip()
            student_id = int(line[:3])
            student_name = line[3:]
            students[student_id] = student_name
    return students



def read_assignments():
    assignments = {}
    with open("data/assignments.txt", "r") as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            name = lines[i].strip()
            assignment_id = int(lines[i + 1].strip())
            points = int(lines[i + 2].strip())
            assignments[assignment_id] = {"name": name, "points": points}
    return assignments



def read_submissions():
    submissions = []
    submissions_dir = "data/submissions"
    for filename in os.listdir(submissions_dir):
        file_path = os.path.join(submissions_dir, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                for line_number, line in enumerate(file, start=1):
                    line = line.strip()
                    if line:
                        parts = line.split("|")
                        if len(parts) == 3:
                            try:
                                student_id = int(parts[0].strip())
                                assignment_id = int(parts[1].strip())
                                percentage = float(parts[2].strip())
                                submissions.append((student_id, assignment_id, percentage))
                            except ValueError:
                                print(f"Skipping invalid data in {filename}, line {line_number}: {line}")
                        else:
                            print(f"Skipping improperly formatted line in {filename}, line {line_number}: {line}")
    return submissions



def main():
    students = read_students()
    assignments = read_assignments()
    submissions = read_submissions()

    menu = """
1. Student grade
2. Assignment statistics
3. Assignment graph

Enter your selection: """
    choice = input(menu).strip()

    if choice == "1":
        student_name = input("What is the student's name: ").strip()
        student_id = next((id_ for id_, name in students.items() if name == student_name), None)
        if student_id is None:
            print("Student not found")
        else:
            total_score = sum(
                (sub[2] / 100) * assignments[sub[1]]["points"]
                for sub in submissions if sub[0] == student_id
            )
            grade_percentage = round((total_score / 1000) * 100)
            print(f"{int(grade_percentage)}%")
    elif choice == "2":
        assignment_name = input("What is the assignment name: ").strip()
        assignment_id = next((id_ for id_, info in assignments.items() if info["name"] == assignment_name), None)
        if assignment_id is None:
            print("Assignment not found")
        else:
            scores = [sub[2] for sub in submissions if sub[1] == assignment_id]
            print(f"Min: {int(min(scores))}%")
            print(f"Avg: {int(sum(scores) / len(scores))}%")
            print(f"Max: {int(max(scores))}%")
    elif choice == "3":
        assignment_name = input("What is the assignment name: ").strip()
        assignment_id = next((id_ for id_, info in assignments.items() if info["name"] == assignment_name), None)
        if assignment_id is None:
            print("Assignment not found")
        else:
            scores = [sub[2] for sub in submissions if sub[1] == assignment_id]
            if scores:

                min_score = min(scores)
                max_score = max(scores)
                bins = range(int(min_score), int(max_score) + 5, 5)

                plt.hist(scores, bins=bins, edgecolor='black')
                plt.title(f"Scores for {assignment_name}")
                plt.xlabel("Score Range")
                plt.ylabel("Frequency")
                plt.show()
            else:
                print(f"No submissions found for {assignment_name}")
    else:
        print("Invalid selection")


if __name__ == "__main__":
    main()
