$( document ).ready(function() {

    // var options = {
        
    //     url: "protected/courses_with_names.json",

    //     getValue: "class",

    //     list: {
    //         maxNumberOfElements: 100,
    //         match: {
    //             enabled: true
    //         }
    //     },

    //     theme: "square"
    // };

    var options = {

        url: "protected/courses_with_names.json",
    
        categories: [{
            listLocation: "courses",
            maxNumberOfElements: 50,
            header: "Courses"
        }, {
            listLocation: "professors",
            maxNumberOfElements: 50,
            header: "Professors"
        }],
    
        getValue: function(element) {
            return element.name;
        },
    
        list: {
            maxNumberOfElements: 100,
            match: {
                enabled: true
            },
            sort: {
                enabled: true
            }
        },
    
        theme: "square"
    };


    $("#majors").easyAutocomplete(options);

    // When enter is pressed
    $(document).on('keypress',function(e) {
        if(e.which == 13) {
            search();
        }
    });

    // When search button is clicked
    $("#submit").click(function(){
        search();
    });

    function search(){
        var search_string = $("#majors").val();
        
        var split_string = search_string.split(" ");

        // Basic sanity check, must include subject & subject number
        if(split_string.length < 2)
            return false;

        if(hasNumber(split_string)){
            // Course
            var subject = split_string[0].toLowerCase();
            var subject_number = split_string[1].toUpperCase();

            var url = window.location.protocol + "//" + window.location.host + "/" + "course" + "/" + subject + "/" + subject_number;
            $(location).attr('href',url);
        }else{
            // Professor
            var url = window.location.protocol + "//" + window.location.host + "/" + "professor" + "/" + search_string
            $(location).attr('href',url);
        }
    }

    function hasNumber(myString) {
        return /\d/.test(myString);
      }

});
