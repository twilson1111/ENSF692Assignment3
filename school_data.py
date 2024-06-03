# school_data.py
# Tom Wilson
#
# A terminal-based application for computing and printing school statistics based on given user-prompted input.
# Once a school is selected, the program will report numerous school specific statistics, and additionally
# statistics for the school system as a whole.  The program terminates upon completion.

import numpy as np
import string

from given_data import year_2013, year_2014, year_2015, year_2016, year_2017, year_2018, year_2019, year_2020, year_2021, year_2022

class School:
    """
    Represents a school including its name and associated school code
    Instance Variables:
    name -- Human readable school name
    code -- Integer school code
    """
    def __init__(self, name, code):
        self.name = name
        self.code = code

# List of all schools
schools = [
    School("Centennial High School", 1224),
    School("Robert Thirsk School", 1679),
    School("Louise Dean School", 9626),
    School("Queen Elizabeth High School", 9806),
    School("Forest Lawn High School", 9813),
    School("Crescent Heights High School", 9815),
    School("Western Canada High School",9816),
    School("Central Memorial High School", 9823),
    School("James Fowler High School",9825),
    School("Ernest Manning High School",9826),
    School("William Aberhart High School",9829),
    School("National Sport School",9830),
    School("Henry Wise Wood High School",9836),
    School("Bowness High School",9847),
    School("Lord Beaverbrook High School",9850),
    School("Jack James High School",9856),
    School("Sir Winston Churchill High School",9857),
    School("Dr. E. P. Scarlett High School",9858),
    School("John G Diefenbaker High School",9860),
    School("Lester B. Pearson High School",9865)
]

# This dictionary is used to organize school data by year.
years_dict = {
    2013: year_2013,
    2014: year_2014,
    2015: year_2015,
    2016: year_2016,
    2017: year_2017,
    2018: year_2018,
    2019: year_2019,
    2020: year_2020,
    2021: year_2021,
    2022: year_2022,

}

# Constants that define the extent of the input data
first_year = 2013
last_year = 2022
first_grade = 10
last_grade = 12

def parse_user_input(input: string):
    """
    Parse user input into a school selection by mapping either the school code or school name.
    Parameter - input: String (The input that was specified by the user)
    Returns - School (the school that was successfully specified)
    Throws ValueError if no school is found that matches the parsed user input
    """
    friendly_input = input.strip().lower()
    for school in schools:
        friendly_school_name = school.name.strip().lower()
        if friendly_school_name == friendly_input or int(friendly_input) == school.code:
            return school
    raise ValueError

def school_slice(the_array, school_index: int):
    """
    Return a sub-view of the input array that represents a specific school.
    Parameters:
        the_array: 3d array containing all school system information
        school_index: The index of the selected school in the 3d array.
    Returns: sub-view of specified data
    """
    return the_array[::1, school_index, ::1]

def grade_slice_at_school(the_array, school_index: int, grade: int):
    """
    Return a sub-view of the input array that represents a specific school and specific grade.
    Parameters:
        the_array: 3d array containing all school system information
        school_index: The index of the selected school in the 3d array.
        grade: the desired grade.
    Returns: sub-view of specified data
    """
    grade_index = grade - first_grade
    school_slc = school_slice(the_array, school_index)
    grade_slc = school_slc[::1, grade_index]
    return grade_slc
    
def year_slice_at_school(the_array, school_index: int, year: int):
    """
    Return a sub-view of the input array that represents a specific school and specific year.
    Parameters:
        the_array: 3d array containing all school system information
        school_index: The index of the selected school in the 3d array.
        year: the desired year.
    Returns: sub-view of specified data
    """
    year_index = year - first_year
    school_slc = school_slice(the_array, school_index)
    year_slc = school_slc[year_index, ::1]
    return year_slc

def year_slice(the_array, year: int):
    """
    Return a sub-view of the input array that represents a specific year.
    Parameters:
        the_array: 3d array containing all school system information
        year: the desired year.
    Returns: sub-view of specified data
    """
    year_index = year - first_year
    year_slc = the_array[year_index, ::1, ::1]
    return year_slc

def grade_slice_for_year(the_array, year: int, grade: int):
    """
    Return a sub-view of the input array that represents a specific year and specific grade.
    Parameters:
        the_array: 3d array containing all school system information
        year: The desired year
        grade: the desired grade.
    Returns: sub-view of specified data
    """
    grade_index = grade - first_grade
    school_slc = year_slice(the_array, year)
    grade_slc = school_slc[::1, grade_index]
    return grade_slc

def grade_slice(the_array, grade: int):
    """
    Return a sub-view of the input array that represents a specific grade.
    Parameters:
        the_array: 3d array containing all school system information
        grade: the desired grade.
    Returns: sub-view of specified data
    """
    grade_index = grade - first_grade
    grade_slc = the_array[::1, ::1, grade_index]
    return grade_slc



def main():

    print("ENSF 692 School Enrollment Statistics")

    # Generate list of data by appending year data chunks.
    years_list = []
    for year in range(first_year, last_year + 1, 1):
        years_list.append(years_dict[year])

    # Convert list to 3d numpy array with indexes (year, school, grade)
    years_np_1d_array = np.array(years_list)
    years_np_3d_array = years_np_1d_array.reshape(10, 20, 3)

    # Report shape and dimension of 3d array
    print("3D Array Shape: ")
    print(years_np_3d_array.shape)
    print("Dimensions of Array:")
    print(years_np_3d_array.ndim)

    # Prompt for user input for selecting a school.  Check whether school exists with parsed input & repeat until satisfied.
    selected_school = None
    while selected_school == None:
        print("Please enter the school name or code:")
        user_input = input(" >")
        try:
            selected_school = parse_user_input(user_input)
        except ValueError:
            print("You must enter a valid school name or code.")
            print("Please try again...\n")
    school_index = schools.index(selected_school)

    # Print various school-specific statistics by grade, year and over entire school.
    print("\n***Requested School Statistics***\n")
    print("School Name: " + selected_school.name)
    print("School code: " + str(selected_school.code))
    school_data = school_slice(years_np_3d_array, school_index)
    for grade in (10, 11, 12):
        grade_data = grade_slice_at_school(years_np_3d_array, school_index, grade)
        print("Mean Enrollment for Grade " + str(grade) + ": " + str(int(np.nanmean(grade_data))))
    print("Highest Enrollment for Any Grade: " + str(int(np.nanmax(school_data))))
    print("Lowest Enrollment for Any Grade: " + str(int(np.nanmin(school_data))))
    for year in range(first_year, last_year + 1, 1):
        year_data = year_slice_at_school(years_np_3d_array, school_index, year)
        print("Total Enrollment for " + str(year) + ": " + str(int(np.nansum(year_data))))
    
    # Print statistics for entire data set (all schools)
    print("Total 10 Year Enrollment: " + str(int(np.nansum(school_data))))
    print("Mean Total Enrollment over 10 Years: " + str(int(np.mean(np.nansum(school_data,axis=1)))))
    enrollments_over_500 = school_data[school_data > 500]
    if len(enrollments_over_500) == 0:
        print("No enrollments over 500.")
    else:
        print("For all Enrollments over 500, the Median Value was: " + str(int(np.nanmedian(enrollments_over_500))))
    print("\n***General Statistics for All Schools***\n")
    print("Mean Enrollment in 2013: " + str(int(np.nanmean(year_slice(years_np_3d_array, 2013)))))
    print("Mean Enrollment in 2022: " + str(int(np.nanmean(year_slice(years_np_3d_array, 2022)))))
    print("Total Graduating Class of 2022: " + str(int(np.nansum(grade_slice_for_year(years_np_3d_array, 2022, 12)))))
    print("Highest Enrollment for a Single Grade: " + str(int(np.nanmax(years_np_3d_array))))
    print("Lowest Enrollment for a Single Grade: " + str(int(np.nanmin(years_np_3d_array))))

if __name__ == '__main__':
    main()

