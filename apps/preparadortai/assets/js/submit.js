function SubmitFormData() {
    var bloque = $("#bloque").val();
    var tema = $("#tema").val();
    var categoria = $("#categoria").val();
    var type = $("input[type=radio]:checked").val();
    var pregunta = $("#pregunta").val();
    var correcta = $("#correcta").val();
    var justificacion =  $("#justificacion").val();
    var incorrectasObj = {}; 
    var incorrectasObj =  document.getElementsByName("field_name[]");
    var incorrectasVal = [];
    for (var i = 0; i < incorrectasObj.length; i++) {
        incorrectasVal.push(incorrectasObj[i].value);
    }


    var justifObj = {}; 
    var justifObj =  document.getElementsByName("justif_name[]");
    var justifVal = [];
    for (var i = 0; i < justifObj.length; i++) {
        justifVal.push(justifObj[i].value);
    }
         
    $.post("submit.php", { bloque: bloque, tema: tema, categoria: categoria, type: type, pregunta: pregunta, correcta: correcta, justificacion: justificacion,incorrectas: incorrectasVal, justif: justifVal},
    function(data) {
	 $('#results').html(data);    
    });

}