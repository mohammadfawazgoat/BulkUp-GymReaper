# BulkUp: GymReaper

#### Video Demo: [https://youtu.be/4T4zizVljX8](https://youtu.be/4T4zizVljX8)

## Description

BulkUp: GymReaper is a comprehensive fitness and gym management web application built using HTML, CSS, JavaScript, Flask, and SQL. The aim of the project is to create an all-in-one platform where both gym users and administrators can interact with data relevant to fitness goals, workout routines, dietary intake, and fee management. The system offers a digital solution to replace the traditional pen-and-paper tracking of gym activities, progress, and payments.

The website has nine main pages accessible to regular users. The Homepage serves as the landing page, where users can read all essential information about the gym, such as its purpose, available facilities, and motivation. It sets the tone for what the platform offers. From there, users can either log in or register. Upon logging in, they are directed to a fully personalized Dashboard, which displays data such as the number of workouts completed, total calories consumed, and useful shortcuts to other sections of the site.

The Workouts page provides detailed explanations of different training splits like PPL (Push, Pull, Legs) and Bro Split. It also features a quiz or recommendation tool to help users choose the workout split most appropriate for their personal goals and fitness level. This allows for a more tailored approach to training, making it easier for beginners and intermediates to stick to a plan.

The Workout Tracker allows users to log their daily exercises, including exercises performed, sets, reps, and weights used. Once workouts are logged, users can view their full Workout History, which keeps a chronological record of all their previous training sessions. This feature helps users stay consistent and accountable, while also letting them reflect on how their training has evolved over time.

There’s also a Progress Graph page, which visually represents the user’s performance over time. This might include the number of workouts done per week, total volume lifted, or other relevant statistics. It serves as a motivational tool to see visible progress in one’s fitness journey.

The Diet Tracker helps users monitor what they eat by providing nutritional information about various food items, such as calories, proteins, carbs, and fats. This feature is especially useful for people who are cutting or bulking, as it allows them to stay within their target calorie range. Users can also enter and store their meals and get summaries based on what they consumed.

On the Personal Info page, users can input their age, weight, height, fitness goals (e.g., weight loss, maintenance, or bulking), and other details. These values are used to personalize the experience further and allow the system to calculate basic maintenance calories or progress expectations.

There’s also a Profile Page accessed via the username tab, where users can view their stored information, such as current goals, personal stats, and their monthly fee payment status. This area provides an overview of everything the user has done on the site.

For gym owners or staff, there are two extra pages available only when logged in as an admin user. The first is the Admin Page, which allows the admin to mark which users have paid their monthly gym fees. Instead of writing names in a physical register, the admin can update this directly on the site. The second page is the Fees Paid tab, which displays a list of all users who have paid. This simplifies the gym’s fee tracking process and ensures a reliable digital record is always available.

Developing BulkUp: GymReaper was both challenging and rewarding. It required implementing user authentication using Flask sessions, setting up a robust SQL database to store workouts, meals, and user information, and managing different user roles (normal users vs admin) using conditional rendering.
