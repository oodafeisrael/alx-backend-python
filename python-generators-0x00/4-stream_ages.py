#!/usr/bin/python3
import seed

def stream_user_ages():
    """Generator that yields user ages one by one."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    
    for (age,) in cursor:
        yield float(age)  # convert to float if needed for division
    
    cursor.close()
    connection.close()

def calculate_average_age():
    total = 0
    count = 0
    
    for age in stream_user_ages():
        total += age
        count += 1
    
    if count > 0:
        average = total / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users in database.")

# Run the function
if __name__ == "__main__":
    calculate_average_age()
