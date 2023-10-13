<!DOCTYPE html>
<head><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
<link rel="stylesheet" type="text/css" media="print" href='https://servicios.rpba.gob.ar/style/comun/styleServiciosWeb2011Print.min.css' />
<link rel="stylesheet" type="text/css" media="screen" href='https://servicios.rpba.gob.ar/style/comun/SiteMesh.php?decorator=identity' />
<style type="text/css">
#toolbar1{background-color: rgba(51,51,51,0.52);color:#FFF;height:45px;}
#toolbar1 ul{margin:0;padding: 0;list-style: none;}
#toolbar1 li{display: inline;margin: 0 0 0 0;padding: 0;text-transform:uppercase;}
#toolbar1 a{float: left;display: block;color: #FFFFFF;text-decoration: none;margin: 0 0 0 0;padding: 10px 10px;}
#toolbar1 a:hover{background-color:rgba(51,51,51,0.42)}
</style>
</head>


<body class="--bs-info">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz" crossorigin="anonymous"></script>    
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
			</ul>
		</td>
		<TD width="26%" style="text-align: right;">
			<FONT color="#fdfdfd" size="2" face="Tahoma">
				Martes, 3 de Octubre de 2023								
			</font>
		</td>
	</tr>
</table>
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

    </body>