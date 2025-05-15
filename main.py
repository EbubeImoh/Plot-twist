from plotwist import plot_from_csv

csv_file = "students_social_media_addiction.csv"
user_query = "show me the different age groups and their social media addiction levels"

plot_from_csv(csv_file, user_query, show_code=False)