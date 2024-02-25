<!DOCTYPE html>
<html lang="es">
<head>
<title>Página de búsqueda</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
<link rel="stylesheet" type="text/css" media="print" href='https://servicios.rpba.gob.ar/style/comun/styleServiciosWeb2011Print.min.css' />
<link rel="stylesheet" type="text/css" media="screen" href='https://servicios.rpba.gob.ar/style/comun/SiteMesh.php?decorator=identity' />
<style type="text/css">
#ayuda-mensaje {
    position: absolute;
    background-color: #a5e2e6;
    border: 1px solid #ccc;
    padding: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    z-index: 1000;
	text-align: left; /* Alineación a la izquierda */
}
#toolbar1{background-color: rgba(51,51,51,0.52);color:#FFF;height:45px;}
#toolbar1 ul{margin:0;padding: 0;list-style: none;}
#toolbar1 li{display: inline;margin: 0 0 0 0;padding: 0;text-transform:uppercase;}
#toolbar1 a{float: left;display: block;color: #FFFFFF;text-decoration: none;margin: 0 0 0 0;padding: 10px 10px;}
#toolbar1 a:hover{background-color:rgba(51,51,51,0.42)}
</style>
</head>


<body class="--bs-info">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz" crossorigin="anonymous" defer></script>
<!-- #main-navigation -->
<div id="contenedor">
		<div id="title">
		<div style="background-color: #009aae;">

<!--<a href="https://www.ec.gba.gov.ar">-->
<a href="https://www.gba.gob.ar/hacienda_y_finanzas">
		<img src="https://servicios.rpba.gob.ar/images/comun/logo_gba_footer_blanco.png" alt="Ministerio de Economía de la Provincia de Buenos Aires" style="border:0px;height:95px;margin-left:10px">
</a>
</div>
<TABLE id="toolbar1" width="100%">
	<tr>
		<td>
		<ul>
		<li><a title="Inicio" href='/index.php'>INICIO</a></li>
        <li><a title='Gobierno de la Provincia de Buenos Aires' target="_blank" href='http://www.gba.gov.ar'>PORTAL DE LA PROVINCIA</a></li>
		<li>
    		<!-- Elemento de ayuda -->
    		<a id="ayuda-icono" title="Ayuda">ℹnformación</a>
  		</li>
	
		</ul>
		</td>
		<TD id="fecha-actual" width="26%" style="text-align: right;">
  			<FONT color="#fdfdfd" size="2" face="Tahoma">
   			 <!-- La fecha actual se actualizará aquí -->
  			</font>
		</td>
	</tr>
</table>

<div id="ayuda-mensaje" class="d-none" >
  <p>Complete el campo de búsqueda luego de titular a <br>
  buscar con el nombre de la persona humana<br>
  o razón social que se encuentra en el formulario<br>
  773, en el rubro Titulares y observaciones
  </p>
  <!-- Agrega más contenido descriptivo según sea necesario -->
</div>


<!-- EOF: #main-navigation -->

    <nav class="navbar bg-body-tertiary" data-bs-theme="--bs-info">
    <div class="container-fluid justify-content-center">
    <form action="{{ url_for('matricula')}}" method="post" class="d-flex align-items-center">
        <div class="input-group">
          <span class="input-group-text">Titular a buscar</span>
          <input type="text" name="cadena" class="form-control"></input>
        </div>
        <button class="btn btn-outline-success ms-2">Enviar</button>
      </form>
    </div>
    </nav>

	<script>
	  document.getElementById('ayuda-icono').addEventListener('click', function() {
    	var ayudaMensaje = document.getElementById('ayuda-mensaje');
    	ayudaMensaje.classList.toggle('d-none');
  		});
	</script>
    <script>
  		// Obtenemos el elemento que contiene la fecha
 		 var fechaActualElement = document.getElementById('fecha-actual');

 		 // Obtenemos la fecha actual
 		var fechaActual = new Date();

  		// Formateamos la fecha según tu preferencia
  		var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
  		var fechaFormateada = fechaActual.toLocaleDateString('es-ES', options);

  		// Actualizamos el contenido del elemento con la fecha formateada
  		fechaActualElement.innerHTML = fechaFormateada;
</script>
</body>

</html>