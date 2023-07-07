<!DOCTYPE html>
<head><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
</head>


<body class="--bs-info">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz" crossorigin="anonymous"></script>    
<!-- #main-navigation -->
<div id="main-navigation" class="">
	<div class="container">
		<a class="navbar-brand" href="https://www.gba.gob.ar/"><img
				src="https://gba.gob.ar/imagenes/logo_gba_footer_blanco.svg" alt="logo buenos aires provincia"     style="width: 240px !important;height: auto !important;padding-left: unset !important;margin-left: 0px;"></a>

		<!-- #main-navigation-inside -->
	</div>
</div>
<!-- EOF: #main-navigation -->

    <nav class="navbar bg-body-tertiary" data-bs-theme="--bs-info">
    <div class="container-fluid" >
    <form action="{{ url_for('matricula')}}" method="post" class="d-flex align-items-center">
        <div class="input-group">
          <span class="input-group-text">Buscar</span>
          <input type="text" name="cadena" class="form-control"></input>
        </div>
        <button class="btn btn-outline-success ms-2">Enviar</button>
      </form>
    </div>
    </nav>

    </body>