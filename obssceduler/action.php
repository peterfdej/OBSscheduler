<?php

//action.php

include('database_connection.php');

if(isset($_POST["action"]))
{
	if($_POST["action"] == "insert")
	{
		$query = "
	INSERT INTO scedules (swdate, swtime, scene, transition, sourceoff, sourceon, duration, processed) VALUES ('".$_POST["swdate"]."','".$_POST["swtime"]."','".$_POST["scene"]."','".$_POST["transition"]."','".$_POST["sourceoff"]."','".$_POST["sourceon"]."','".$_POST["duration"]."','0')
		";
		$statement = $connect->prepare($query);
		$statement->execute();
		echo '<p>Data Inserted...</p>';
	}
	if($_POST["action"] == "fetch_single")
	{
		$query = "
		SELECT * FROM scedules WHERE id = '".$_POST["id"]."'
		";
		$statement = $connect->prepare($query);
		$statement->execute();
		$result = $statement->fetchAll();
		foreach($result as $row)
		{
			$output['swdate'] = $row['swdate'];
			$output['swtime'] = $row['swtime'];
			$output['scene'] = $row['scene'];
			$output['transition'] = $row['transition'];
			$output['sourceoff'] = $row['sourceoff'];
			$output['sourceon'] = $row['sourceon'];
			$output['duration'] = $row['duration'];
			$output['processed'] = $row['processed'];
		}
		echo json_encode($output);
	}
	if($_POST["action"] == "update")
	{
		$query = "
		UPDATE scedules 
		SET swdate = '".$_POST["swdate"]."',
		swtime = '".$_POST["swtime"]."',
		scene = '".$_POST["scene"]."',
		transition = '".$_POST["transition"]."',
		sourceoff = '".$_POST["sourceoff"]."',
		sourceon = '".$_POST["sourceon"]."',
		duration = '".$_POST["duration"]."'
		WHERE id = '".$_POST["hidden_id"]."'
		";
		$statement = $connect->prepare($query);
		$statement->execute();
		echo '<p>Data Updated</p>';
	}
	if($_POST["action"] == "delete")
	{
		$query = "DELETE FROM scedules WHERE id = '".$_POST["id"]."'";
		$statement = $connect->prepare($query);
		$statement->execute();
		echo '<p>Data Deleted</p>';
	}
}

?>