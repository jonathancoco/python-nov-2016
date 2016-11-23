
$(document).ready(function () {


    $('#dataSearch').submit(function()
        {
    
            if ( ($('#property_id').val() == '') &
                 ($('#geo_id').val() == '') &
                 ($('#dba_name').val() == '') &
                 ($('#street_number').val() == '') &
                 ($('#street_name').val() == '') &
                 ($('#owner_name').val() == ''))
            {
                var strErrorMessage = "You must specify at least one search criteria! ";

                alert(strErrorMessage);

                return false;
            }

            return true;
        }

    )

    $('#dataClear').submit(function()
        {
            $("#property_id").val('');
            $("#geo_id").val('');
            $("#owner_name").val('');
            $("#dba_name").val('');
            $("#street_number").val('');
            $("#street_name").val('');

            return false;
        }
    )
})
