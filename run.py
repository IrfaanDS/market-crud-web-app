from market import app

# Checks if the run.py file has executed directly and not imported
if __name__ == '__main__':
    # CRITICAL FIX: Ensure 'host=0.0.0.0' is present
    app.run(host='0.0.0.0', port=5000, debug=False)
