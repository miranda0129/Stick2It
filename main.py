
if __name__ == "__main__":
    import sys
    from widgets import app 
    new_app, window = app.run()
    sys.exit(new_app.exec_())