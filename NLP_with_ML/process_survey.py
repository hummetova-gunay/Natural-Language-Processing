import pandas as pd
import os
from pathlib import Path

def process_teacher_csvs(folder_path):
    """
    Process CSV files from a folder to create a dataset with teacher metrics.
    
    Parameters:
    -----------
    folder_path : str
        Path to the folder containing CSV files (teacher names as filenames)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with columns: Name, Instructor_Skill, Interaction, 
        Student_Motivation, Course_Organization
    
    CSV Structure Expected:
    - First 5 rows AVG values -> Instructor_Skill
    - Next 6 rows AVG values -> Interaction (rows 5-10)
    - Next 4 rows AVG values -> Student_Motivation (rows 11-14)
    - Next 6 rows AVG values -> Course_Organization (rows 15-20)
    """
    
    # Initialize lists to store data
    data = {
        'Name': [],
        'Instructor_Skill': [],
        'Interaction': [],
        'Student_Motivation': [],
        'Course_Organization': []
    }
    
    # Get all CSV files in the folder
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    
    print(f"Found {len(csv_files)} CSV files in {folder_path}")
    print("=" * 80)
    
    for csv_file in csv_files:
        # Extract teacher name from filename (remove .csv extension)
        teacher_name = csv_file.replace('.csv', '')
        
        # Read the CSV file
        file_path = os.path.join(folder_path, csv_file)
        df = pd.read_csv(file_path)
        
        # Check if AVG column exists
        if 'AVG' not in df.columns:
            print(f"Warning: 'AVG' column not found in {csv_file}. Skipping...")
            continue
        
        # Extract AVG values for different categories
        try:
            # Instructor Skill: rows 0-4 (first 5 rows)
            instructor_skill = df['AVG'].iloc[0:5].mean()
            
            # Interaction: rows 5-10 (next 6 rows)
            interaction = df['AVG'].iloc[5:11].mean()
            
            # Student Motivation: rows 11-14 (next 4 rows)
            student_motivation = df['AVG'].iloc[11:15].mean()
            
            # Course Organization: rows 15-20 (next 6 rows)
            course_organization = df['AVG'].iloc[15:21].mean()
            
            # Append to data dictionary
            data['Name'].append(teacher_name)
            data['Instructor_Skill'].append(instructor_skill)
            data['Interaction'].append(interaction)
            data['Student_Motivation'].append(student_motivation)
            data['Course_Organization'].append(course_organization)
            
            print(f"✓ Processed: {teacher_name}")
            print(f"  Instructor_Skill: {instructor_skill:.2f}")
            print(f"  Interaction: {interaction:.2f}")
            print(f"  Student_Motivation: {student_motivation:.2f}")
            print(f"  Course_Organization: {course_organization:.2f}")
            print()
            
        except IndexError as e:
            print(f"Error processing {csv_file}: Not enough rows in AVG column")
            print(f"  Expected at least 21 rows, found {len(df)}")
            print()
            continue
    
    # Create DataFrame
    result_df = pd.DataFrame(data)
    
    print("=" * 80)
    print(f"Successfully processed {len(result_df)} teachers")
    
    return result_df


# Example usage:
if __name__ == "__main__":
    # Specify the folder path containing CSV files
    folder_path = "teacher_data"  # Change this to your folder path
    
    # Process the CSV files
    teacher_metrics_df = process_teacher_csvs(folder_path)
    
    # Display the resulting dataframe
    print("\n" + "=" * 80)
    print("FINAL DATASET")
    print("=" * 80)
    print(teacher_metrics_df.to_string(index=False))
    
    # Optional: Save to CSV
    output_file = "teacher_metrics.csv"
    teacher_metrics_df.to_csv(output_file, index=False)
    print(f"\n✓ Dataset saved to {output_file}")
    
    # Display summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print(teacher_metrics_df.describe())


# Alternative version with more flexible row ranges
def process_teacher_csvs_custom(folder_path, row_ranges):
    """
    Process CSV files with custom row ranges for each metric.
    
    Parameters:
    -----------
    folder_path : str
        Path to the folder containing CSV files
    row_ranges : dict
        Dictionary specifying row ranges for each metric
        Example: {
            'Instructor_Skill': (0, 5),
            'Interaction': (5, 11),
            'Student_Motivation': (11, 15),
            'Course_Organization': (15, 21)
        }
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with teacher metrics
    """
    
    data = {
        'Name': [],
        **{metric: [] for metric in row_ranges.keys()}
    }
    
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    
    for csv_file in csv_files:
        teacher_name = csv_file.replace('.csv', '')
        file_path = os.path.join(folder_path, csv_file)
        df = pd.read_csv(file_path)
        
        if 'AVG' not in df.columns:
            continue
        
        try:
            data['Name'].append(teacher_name)
            
            for metric, (start, end) in row_ranges.items():
                avg_value = df['AVG'].iloc[start:end].mean()
                data[metric].append(avg_value)
                
        except IndexError:
            print(f"Error: {csv_file} doesn't have enough rows")
            # Remove the last added name if error occurs
            data['Name'].pop()
            continue
    
    return pd.DataFrame(data)