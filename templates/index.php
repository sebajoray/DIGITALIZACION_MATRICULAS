<!DOCTYPE html>
<body>
    <h1 style='color:red'>Cadena a buscar:</h1>
    <form action="{{ url_for('matricula')}}" method="post">
    <h2><input type="texto" name="cadena"></input>
        <button>Enviar</button> </h2>
    </form>
    {{result}}
</body>
