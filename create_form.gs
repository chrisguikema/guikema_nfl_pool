function createForms() {

    var files = DriveApp.getFiles();

    while (files.hasNext()) {
        var file = files.next();
        var name = file.getName();
        var week = 0;

        for (week = 1; week < 18; week++) {
            var sched = name.search("Week " + week + " - sched.csv");
            if (sched == 0) {
                break;
            }
        }

        if (sched == 0) {
            var form = FormApp.create("Week" + week);
            var sheet = SpreadsheetApp.open(file).getSheets()[0];
            var range = sheet.getDataRange();
            var values = range.getValues();

            var num_games = values[0].length;

            form.setTitle('Week ' + week + " Picks")
                .setDescription('NFL Picks for Week ' + week)
                .setConfirmationMessage('Good Luck!')
                .setAllowResponseEdits(false)
                .setAcceptingResponses(true);

            var item = form.addMultipleChoiceItem();
            item.setChoices([
              item.createChoice('Curt'),
              item.createChoice('Amy'),
              item.createChoice('Laura'),
              item.createChoice('Tyler'),
              item.createChoice('Katie'),
              item.createChoice('Troy'),
              item.createChoice('Chris'),
              item.createChoice('Sam'),
            ]);

            for (var i = 0; i < num_games; i++) {
                var item = form.addMultipleChoiceItem();
                item.setChoices([
                    item.createChoice(values[0][i]),
                    item.createChoice(values[1][i])
                ]);
            }
        }
    }
};
