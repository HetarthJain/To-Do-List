from website import create_app
# the website is python package, so when we call the create_app it automatically runs the init file. 
app =  create_app()

if __name__ == '__main__':
	app.run(debug=True)
