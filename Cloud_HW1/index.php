<!DOCTYPE html>
<html>
  <head>
    <title>Just Kidding</title>
    <link rel="stylesheet" href="stylish.css">
  </head>
  <body>
    <h1>Click the image to gain a random cat fact!</h1>
    <form action="index.php" method="post">
      <input type="image" align="middle" src="internet.png" alt="Submit" /><br>
      <input type="hidden" name="imgy" value="imgy" />
    </form>
    <h2>
      <?php if( isset($_POST["imgy"])){
        include("felineFactFlinger.php");
      }
      ?>
      <br></br>
      <form action="index.php" method="post">
        Enter Your First Name: <input type="Text" name="first" align="middle">
        <input type="Submit" value="Catify!"><br>
      </form>
      <?php
        if( isset($_POST["first"])){
          include("catify.php");
        }
      ?>
    </h2>
  </body>
</html>
