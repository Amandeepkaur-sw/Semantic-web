from flask import Flask, request, render_template
from rdflib import Graph
import os

app = Flask(__name__)

# Load RDF data in the appropriate format based on file extension
def load_rdf(file_path):
    g = Graph()

    # Determine the file format based on the file extension
    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.ttl':
        format = 'turtle'
    elif ext in ['.rdf', '.xml']:
        format = 'xml'
    else:
        raise ValueError(f"Unsupported file format: {ext}")

    # Parse the RDF file with the determined format
    g.parse(file_path, format=format)
    return g

# Execute SPARQL query
def execute_query(graph, query):
    results = graph.query(query)
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    rdf_file = request.files['rdf_file']
    sparql_query = request.form['sparql_query']
    
    # Save the uploaded RDF file temporarily
    rdf_file_path = os.path.join('uploads', rdf_file.filename)
    rdf_file.save(rdf_file_path)
    
    try:
        # Load RDF data based on the file format
        g = load_rdf(rdf_file_path)
        
        # Execute SPARQL query
        results = execute_query(g, sparql_query)
        
    except Exception as e:
        return f"An error occurred while processing the query: {e}"
    
    finally:
        # Delete the temporary file after processing
        if os.path.exists(rdf_file_path):
            os.remove(rdf_file_path)
    
    return render_template('results.html', results=results)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
