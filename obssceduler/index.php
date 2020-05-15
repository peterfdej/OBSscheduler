<html>  
    <head>  
        <title>OBS sceduler</title>  
		<link rel="stylesheet" href="jquery-ui.css">
        <link rel="stylesheet" href="bootstrap.min.css" />
		<script src="jquery.min.js"></script>  
		<script src="jquery-ui.js"></script>
    </head>  
    <body>  
        <div class="container">
			<br />
			
			<h3 align="center">OBS sceduler</a></h3><br />
			<br />
			<div align="right" style="margin-bottom:5px;">
			<button type="button" name="add" id="add" class="btn btn-success btn-xs">Add</button>
			</div>
			<div class="table-responsive" id="user_data">
				
			</div>
			<br />
		</div>
		
		<div id="user_dialog" title="Bewerk">
			<form method="post" id="user_form">
				<?php
					include("database_connection.php");
					$query = "SELECT * FROM scedules WHERE processed = 0 order by id desc limit 1";
					$statement = $connect->prepare($query);
					$statement->execute();
					$result = $statement->fetchAll();
					$total_row = $statement->rowCount();
					foreach($result as $lastrow)
					{
						$durationseconds = date("s",strtotime($lastrow["duration"])) + (60*(date("i",strtotime($lastrow["duration"]))))+ (60*60*(date("H",strtotime($lastrow["duration"]))));
						$swtimenew = date("H:i:s",strtotime($lastrow["swtime"]) + $durationseconds);
					}
				?>
				<div class="form-group">
					<label>Geef datum</label>
					<input type="date" name="swdate" id="swdate" value="<?php echo date("Y-m-d"); ?>" class="form-control" />
					<span id="error_swdate" class="text-danger"></span>
				</div>
				<div class="form-group">
					<label>Geef tijd</label>
					<input type="time" name="swtime" id="swtime" step="1" value="<?php echo $swtimenew; ?>" class="form-control" />
					<span id="error_swtime" class="text-danger"></span>
				</div>
				<div class="form-group">
					<label>Scene</label>
					<?php
					$query = "SELECT * FROM scenenames";
					$statement = $connect->prepare($query);
					$statement->execute();
					$result = $statement->fetchAll();
					$total_row = $statement->rowCount();?>
					<select name="scene" id="scene" class="form-control" />
						<?php
						if($total_row > 0)
						{
							foreach($result as $row)
								{
								?><option value="<?php echo $row["scene"];?>"><?php echo $row["scene"];?></option><?php
								}
						}
						?>
					</select>
					<span id="error_scene" class="text-danger"></span>
				</div>
				<div class="form-group">
					<label>Transitie</label>
					<?php
					$query = "SELECT * FROM transitionnames";
					$statement = $connect->prepare($query);
					$statement->execute();
					$result = $statement->fetchAll();
					$total_row = $statement->rowCount();?>
					<select name="transition" id="transition" class="form-control">
						<?php
						if($total_row > 0)
						{
							foreach($result as $row)
								{
								?><option value="<?php echo $row["transition"];?>"><?php echo $row["transition"];?></option><?php
								}
						}
						?>
					</select> 
					<span id="error_transition" class="text-danger"></span>
				</div>
				<div class="form-group">
					<label>Bron uit</label>
					<?php
					$query = "SELECT * FROM sourcenames";
					$statement = $connect->prepare($query);
					$statement->execute();
					$result = $statement->fetchAll();
					$total_row = $statement->rowCount();?>
					<select name="sourceoff" id="sourceoff" class="form-control" />
						<option value=""></option>
						<?php
						if($total_row > 0)
						{
							foreach($result as $row)
								{
								?><option value="<?php echo $row["source"];?>"><?php echo $row["scene"] . " &nbsp;|" . $row["source"];?></option><?php
								}
						}
						?>
					</select>
					<span id="error_sourceoff" class="text-danger"></span>
				</div>
				<div class="form-group">
					<label>Bron aan</label>
					<select name="sourceon" id="sourceon" class="form-control" />
						<option value=""></option>
						<?php
						if($total_row > 0)
						{
							foreach($result as $row)
								{
								?><option value="<?php echo $row["source"];?>"><?php echo $row["scene"] . " |" . $row["source"];?></option><?php
								}
						}
						?>
					</select>
					<span id="error_sourceon" class="text-danger"></span>
				</div>
				<div class="form-group">
					<label>Geef looptijd</label>
					<input type="time" name="duration" id="duration" step="1" value="00:00:00" class="form-control" />
					<span id="error_duration" class="text-danger"></span>
				</div>
				<div class="form-group">
					<label>Geef herhaaltijd in uren</label>
					<input type="text" name="repeattime" id="repeattime" class="form-control" />
					<span id="error_repeattime" class="text-danger"></span>
				</div>
				<div class="form-group">
					<input type="hidden" name="action" id="action" value="insert" />
					<input type="hidden" name="hidden_id" id="hidden_id" />
					<input type="submit" name="form_action" id="form_action" class="btn btn-info" value="Insert" />
				</div>
			</form>
		</div>
		
		<div id="action_alert" title="Action">
			
		</div>
		
		<div id="delete_confirmation" title="Confirmation">
		<p>Are you sure you want to Delete this data?</p>
		</div>
		
    </body>  
</html>  




<script>  
$(document).ready(function(){  

	load_data();
    
	function load_data()
	{
		$.ajax({
			url:"fetch.php",
			method:"POST",
			success:function(data)
			{
				$('#user_data').html(data);
			}
		});
	}
	
	$("#user_dialog").dialog({
		autoOpen:false,
		width:400
	});
	
	$('#add').click(function(){
		$('#user_dialog').attr('title', 'Add Data');
		$('#action').val('insert');
		$('#form_action').val('Toevoegen');
		$('#user_form')[0].reset();
		$('#form_action').attr('disabled', false);
		$("#user_dialog").dialog('open');
	});
	
	$('#user_form').on('submit', function(event){
		event.preventDefault();
		var error_swdate = '';
		var error_scene = '';
		if($('#swdate').val() == '')
		{
			error_dswdate = 'Datum is noodzakelijk';
			$('#error_swdate').text(error_swdate);
			$('#swdate').css('border-color', '#cc0000');
		}
		else
		{
			error_swdate = '';
			$('#error_swdate').text(error_swdate);
			$('#dtime').css('border-color', '');
		}
		if($('#scene').val() == '')
		{
			error_scene = 'Scene is noodzakelijk';
			$('#error_scene').text(error_scene);
			$('#scene').css('border-color', '#cc0000');
		}
		else
		{
			error_scene = '';
			$('#error_scene').text(error_scene);
			$('#scene').css('border-color', '');
		}
		
		if(error_swdate != '' || error_scene != '')
		{
			return false;
		}
		else
		{
			$('#form_action').attr('disabled', 'disabled');
			var form_data = $(this).serialize();
			$.ajax({
				url:"action.php",
				method:"POST",
				data:form_data,
				success:function(data)
				{
					$('#user_dialog').dialog('close');
					$('#action_alert').html(data);
					$('#action_alert').dialog('open');
					load_data();
					$('#form_action').attr('disabled', false);
				}
			});
		}
		
	});
	
	$('#action_alert').dialog({
		autoOpen:false
	});
	
	$(document).on('click', '.edit', function(){
		var id = $(this).attr('id');
		var action = 'fetch_single';
		$.ajax({
			url:"action.php",
			method:"POST",
			data:{id:id, action:action},
			dataType:"json",
			success:function(data)
			{
				$('#swdate').val(data.swdate);
				$('#swtime').val(data.swtime);
				$('#scene').val(data.scene);
				$('#transition').val(data.transition);
				$('#sourceoff').val(data.sourceoff);
				$('#sourceon').val(data.sourceon);
				$('#duration').val(data.duration);
				$('#repeattime').val(data.repeattime);
				$('#user_dialog').attr('title', 'Edit Data');
				$('#action').val('update');
				$('#hidden_id').val(id);
				$('#form_action').val('Opslaan');
				$('#user_dialog').dialog('open');
			}
		});
	});
	
	$('#delete_confirmation').dialog({
		autoOpen:false,
		modal: true,
		buttons:{
			Ok : function(){
				var id = $(this).data('id');
				var action = 'delete';
				$.ajax({
					url:"action.php",
					method:"POST",
					data:{id:id, action:action},
					success:function(data)
					{
						$('#delete_confirmation').dialog('close');
						$('#action_alert').html(data);
						$('#action_alert').dialog('open');
						load_data();
					}
				});
			},
			Cancel : function(){
				$(this).dialog('close');
			}
		}	
	});
	
	$(document).on('click', '.delete', function(){
		var id = $(this).attr("id");
		$('#delete_confirmation').data('id', id).dialog('open');
	});
	
});  
</script>