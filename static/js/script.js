        function edit_joueur(no) {
                console.log(no)
                return window.location.replace("/joueurs/edit/" + no);
        }

        /*
        function ouvre_liste(id) {
                //$( "#joueurs_infos_"+id ).toggle();
                console.log("joueurs_infos_"+id)
                //console.log( $( "#joueurs_infos_"+id ).display)
                let el = document.getElementById("joueurs_infos_"+id)
                console.log(el)
                if(el.style.display == 'none') {
                        el.style.display = 'block'
                }
                else {
                        el.style.display = 'none'
                }
                console.log($( "#joueurs_infos_"+id ))
        }
*/
/*   
function ouvre_liste(id) {
      $( "#joueurs_infos_"+id ).toggle()
}

$( ".doodles" ).click(function() {
        if($( this ).html() != "fermer Liste")  $( this ).html("fermer Liste")
        else $( this ).html("afficher Liste")
      });
*/

function ouvre_liste(id) {
        $( ".joueurs_infos_"+id ).toggle()
  }
  
  function ouvre_adresse(id) {
        $( "#adresse_infos_"+id ).toggle()
  }