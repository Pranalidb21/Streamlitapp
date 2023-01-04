import time
import streamlit as st
import hashlib
import streamlit.components.v1 as comp
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import base64
import json
import pandas as pd
st.set_page_config(
		page_title="MyApp",

	)



c=snowflake.connector.connect(
user='team2',
password='KIPIteam2',
account='mw25963.ap-south-1.aws',
warehouse='PC_MATILLION_WH'
)

cx=c.cursor()

cx.execute('use role accountadmin')
cx.execute('CREATE database IF NOT EXISTS  data')

cx.execute('use database data')
cx.execute('use schema public')


def add_userdata(username,password):
	cx.execute('use warehouse PC_MATILLION_WH')
	cx.execute('CREATE TABLE IF NOT EXISTS userstable(username varchar,password varchar)')
	cx.execute('INSERT INTO userstable(username,password) VALUES (%s, %s)', (username,password))
	c.commit()

def login_user(username,password):
	cx.execute('use warehouse PC_MATILLION_WH')

	cx.execute('SELECT * FROM userstable WHERE username =%s AND password =%s',(username,password))
	data = cx.fetchall()
	print(data)
	return data


def view_all_users():
	cx.execute('SELECT * FROM userstable')
	data = cx.fetchall()
	return data

#removing streamlit default properties

st.markdown("""
<style>
.css-9s5bis.edgvbvh3,
.css-1q1n0ol.egzxvld0,
.css-6awftf.e19lei0e1
{
 visibility: hidden;
}
</style>
""",unsafe_allow_html=True)





def main():




	teamtitle = st.empty()
	teamt_clcik = teamtitle.markdown("<h1 style='text-align: center; color:green;'>AKADEMIKS 2.0</h1>",unsafe_allow_html=True)




	menu = ["Home","Student Login","Student SignUp","View Dashboard"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.image("home.jpg")







	elif choice == "Student Login":
		live_style = """

									<style>
									.css-10trblm e16nr0p30{
							    width: 100px;
							    position: relative;
							    display: flex;
							    flex: 1 1 0%;
							    flex-direction: column;
							    gap: 1rem;
							    position: relative;
							    top:80px;
							    left: 30px;
							}
									</style>

							"""
		if teamt_clcik:
			teamtitle.empty()
		secmsg = st.empty()
		secmsg_click = secmsg.subheader("LoginSection")
		if secmsg_click:
			secmsg.empty()

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')


		if st.sidebar.checkbox("Login"):
			live_style = """

							<style>
							.css-1n76uvr {
					    width: 100px;
					    position: relative;
					    display: flex;
					    flex: 1 1 0%;
					    flex-direction: column;
					    gap: 1rem;
					    position: relative;
					    top:-120px;
					    left: -50px;
					}
							</style>

					"""
			st.markdown(live_style, unsafe_allow_html=True)

			st.markdown(live_style, unsafe_allow_html=True)

			# if password == '12345':

			result = login_user(username,password)
			if result:
				sucmsg = st.empty()
				sucmsg_click = sucmsg.success("Logged In as {}".format(username))
				if sucmsg_click:
					sucmsg.empty()

				time.sleep(1)



				def create_table():
					cx.execute(
						'CREATE TABLE IF NOT EXISTS feedback(date_submitted DATE, Q1 TEXT, Q2 TEXT, Q3 NUMBER, Q4 TEXT, Q5 TEXT, Q6 TEXT, Q7 TEXT, Q8 TEXT)')

				def add_feedback(date_submitted, Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8):
					cx.execute(
						'INSERT INTO feedback (date_submitted,Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
						(date_submitted, Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8))
					c.commit()


				st.markdown("<h1 style='text-align: center; color:black;'>Student Feedback Form</h1>", unsafe_allow_html=True)





				d = st.date_input("Today's date", None, None, None, None)



				question_1 = st.text_input('what is your name')
				question_2 = st.text_input('which state do you belong?')
				question_3 = st.slider(
					'Overall, how happy are you with the lesson? (1 very negative,2 negative,3 neutral ,4 positive,5 very positive)', 1,
					5, 1)
				question_4 = st.text_input('How is the teaching?')
				question_5 = st.text_input('what do you think about the course content')
				question_6 = st.text_input('How is the examination pattern?')
				question_7 = st.text_input('How do you feel about the facilities in the lab?')
				question_8 = st.text_input('What could have been better?', max_chars=100)

				if st.button("Submit feedback"):
					create_table()
					add_feedback(d, question_1, question_2, question_3, question_4, question_5, question_6, question_7,
								 question_8)
					st.success("Feedback submitted")






			else:
				st.warning("Incorrect Username/Password")
		else:
			st.header("You must login to view Feedback form ")



	elif choice == "Student SignUp":
		live_style = """

				<style>
				.css-1n76uvr {
		    width: 100px;
		    position: relative;
		    display: flex;
		    flex: 1 1 0%;
		    flex-direction: column;
		    gap: 1rem;
		    position: relative;
		    top:10px;
		    left: -50px;
		}
				</style>

		"""
		st.markdown(live_style, unsafe_allow_html=True)
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):

			add_userdata(new_user,new_password)
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")
	elif  choice == "View Dashboard":



		def checkid(username,password,id):
			cx.execute('use database data')
			cx.execute('use schema public')
			cx.execute('use role accountadmin')
			cx.execute('use warehouse PC_MATILLION_WH')
			cx.execute('SELECT * FROM govtable WHERE username =%s AND password =%s AND id=%s', (username, password,id))
			data = cx.fetchall()
			return data

		login_sidebar=st.sidebar

		username = login_sidebar.text_input("User Name")
		password = login_sidebar.text_input("Password", type='password')
		gvt_id=login_sidebar.text_input("Government Id")
		loginbutton=login_sidebar.button("Login")
		if loginbutton:
			result=checkid(username,password,gvt_id)
			if result:
				login_sidebar.empty()

				teamtitle.empty()

				header=st.empty()
				header1=header.success(f'successfully logged in as {username}')
				time.sleep(1)
				if header1:
					header.empty()



				htmlfile=open("index.html",'r', encoding='utf-8')
				source_code = htmlfile.read()


				comp.html(source_code, width=1105, height=1250,scrolling=False)

				live_style="""
				
		<style>
		.css-1n76uvr {
    width: 100px;
    position: relative;
    display: flex;
    flex: 1 1 0%;
    flex-direction: column;
    gap: 1rem;
    position: relative;
    top: -99px;
    left: -200px;
}
		</style>
		
"""
				st.markdown(live_style,unsafe_allow_html=True)


			else:
				st.write("Invalid username or password")







if __name__ == '__main__':
	main()