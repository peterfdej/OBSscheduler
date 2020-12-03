<?php

//action.php

include('database_connection.php');

if(isset($_POST["action"]))
{
	if($_POST["action"] == "insert")
	{
		$sourceoff = explode("|", $_POST["sourceoff"]);
		$sourceon = explode("|", $_POST["sourceon"]);
		if(count($sourceoff) == 1)
		{
			$qsourceoff = "";
			$qscenesourceoff = "";
		} else
		{
			$qsourceoff = $sourceoff[1];
			$qscenesourceoff = $sourceoff[0];
		}
		if(count($sourceon) == 1)
		{
			$qsourceon = "";
			$qscenesourceon = "";
		} else
		{
			$qsourceon = $sourceon[1];
			$qscenesourceon = $sourceon[0];
		}
		$query = "
		INSERT INTO schedules 
		(swdate, swtime, scene, transition, sourceoff, sourceon, duration, repeattime, processed, scenesourceoff, scenesourceon) 
		VALUES (
		'".$_POST["swdate"]."',
		'".$_POST["swtime"]."',
		'".$_POST["scene"]."',
		'".$_POST["transition"]."',
		'".$qsourceoff."',
		'".$qsourceon."',
		'".$_POST["duration"]."',
		'".$_POST["repeattime"]."',
		'0',
		'".$qscenesourceoff."',
		'".$qscenesourceon."')
		";
		$statement = $connect->prepare($query);
		$statement->execute();
		echo '<p>Data Inserted...</p>';
	}
	if($_POST["action"] == "fetch_single")
	{
		$query = "
		SELECT * FROM schedules WHERE id = '".$_POST["id"]."'
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
			if($row['sourceoff'] == "")
			{
				$output['sourceoff'] = $row['sourceoff'];
			}else
			{
				$output['sourceoff'] = $row["scenesourceoff"] . "|" . $row['sourceoff'];
			}
			if($row['sourceon'] == "")
			{
				$output['sourceon'] = $row['sourceon'];
			}else
			{
				$output['sourceon'] = $row["scenesourceon"] . "|" . $row['sourceon'];
			}
			$output['duration'] = $row['duration'];
			$output['repeattime'] = $row['repeattime'];
		}
		echo json_encode($output);
	}
	if($_POST["action"] == "update")
	{
		$sourceoff = explode("|", $_POST["sourceoff"]);
		$sourceon = explode("|", $_POST["sourceon"]);
		if(count($sourceoff) == 1)
		{
			$qsourceoff = "";
			$qscenesourceoff = "";
		} else
		{
			$qsourceoff = $sourceoff[1];
			$qscenesourceoff = $sourceoff[0];
		}
		if(count($sourceon) == 1)
		{
			$qsourceon = "";
			$qscenesourceon = "";
		} else
		{
			$qsourceon = $sourceon[1];
			$qscenesourceon = $sourceon[0];
		}
		$query = "
		UPDATE schedules 
		SET swdate = '".$_POST["swdate"]."',
		swtime = '".$_POST["swtime"]."',
		scene = '".$_POST["scene"]."',
		transition = '".$_POST["transition"]."',
		sourceoff = '".$qsourceoff."',
		sourceon = '".$qsourceon."',
		duration = '".$_POST["duration"]."',
		repeattime = '".$_POST["repeattime"]."',
		scenesourceoff = '".$qscenesourceoff."',
		scenesourceon = '".$qscenesourceon."'
		WHERE id = '".$_POST["hidden_id"]."'
		";
		$statement = $connect->prepare($query);
		$statement->execute();
		echo '<p>Data Updated</p>';
	}
	if($_POST["action"] == "delete")
	{
		$query = "DELETE FROM schedules WHERE id = '".$_POST["id"]."'";
		$statement = $connect->prepare($query);
		$statement->execute();
		echo '<p>Data Deleted</p>';
	}
}

?>