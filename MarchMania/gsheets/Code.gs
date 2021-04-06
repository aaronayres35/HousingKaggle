// copy-paste code below to a google app script on google sheet

// populate 'header' section with round-by-round results on each bracket sheet
function countColoredCells(wksht, countRange, color="#b7e1cd") {
  var range  = wksht.getRange(countRange);
  var rangeH = range.getHeight();
  var rangeW = range.getWidth();
  
  var bg = range.getBackgrounds();
  var count = 0;
  
  for(var i=0;i<rangeH;i++)
    for(var j=0;j<rangeW;j++)
      if( bg[i][j] == color )
        count=count+1;
  return count;
};
function countCorrectCells(wksht, countRange) { return countColoredCells(wksht, countRange, "#b7e1cd") };
function countWrongCells(wksht, countRange) { return countColoredCells(wksht, countRange, "#f4c7c3") };

function roundCorrect(wksht, l_range, r_range, MAX_N_GAMES) {
  var MAX_PTS_PER_ROUND = 320;
  var PTS_PER_GAME = MAX_PTS_PER_ROUND / MAX_N_GAMES;

  var correctCount = countCorrectCells(wksht, l_range) + countCorrectCells(wksht, r_range);
  var wrongCount   = countWrongCells(wksht, l_range) + countWrongCells(wksht, r_range);
  var n_games_played = correctCount + wrongCount

  return [
    `${(correctCount)}/${n_games_played} (${(100*(correctCount)/n_games_played).toFixed(1)}%)`,
    (correctCount * PTS_PER_GAME),
  ];
};
function roundOf64Correct(wksht) {
  var MAX_N_GAMES = 32
  var l_range = "A5:A67";
  var r_range = "Y5:Y67";

  return roundCorrect(wksht, l_range, r_range, MAX_N_GAMES);
};
function roundOf32Correct(wksht) {
  var MAX_N_GAMES = 16
  var l_range = "C6:C66";
  var r_range = "W6:W66";

  return roundCorrect(wksht, l_range, r_range, MAX_N_GAMES);
};
function sweet16Correct(wksht) {
  var MAX_N_GAMES = 8
  var l_range = "E8:E64";
  var r_range = "U8:U64";

  return roundCorrect(wksht, l_range, r_range, MAX_N_GAMES);
};
function elite8Correct(wksht) {
  var MAX_N_GAMES = 4
  var l_range = "G12:G60";
  var r_range = "S12:S60";

  return roundCorrect(wksht, l_range, r_range, MAX_N_GAMES);
};
function final4Correct(wksht) {
  var MAX_N_GAMES = 2
  var l_range = "I20:I52";
  var r_range = "Q20:Q52";

  return roundCorrect(wksht, l_range, r_range, MAX_N_GAMES);
};
function championshipCorrect(wksht) {
  var MAX_N_GAMES = 1
  var l_range = "K35";
  var r_range = "O35";

  return roundCorrect(wksht, l_range, r_range, MAX_N_GAMES);
};
function totalCorrect(wksht) {
  var range = "A5:Y67"
  var correctCount = countCorrectCells(wksht, range);
  var wrongCount   = countWrongCells(wksht, range);
  var n_games_played = correctCount + wrongCount
  var points = [
    roundOf64Correct(wksht), roundOf32Correct(wksht), sweet16Correct(wksht),
    elite8Correct(wksht), final4Correct(wksht), championshipCorrect(wksht),
  ].map(x => x[1]).reduce((a, b) => a + b, 0);

  return [`${(correctCount)}/${n_games_played} (${(100*(correctCount)/n_games_played).toFixed(1)}%)`, (points)];
};

// populate 'footer' section on summary sheet w/ results from all the brackets
function getSheetUrl(wksht) {
  var url = SpreadsheetApp.getActiveSpreadsheet().getUrl();
  return `${url}#gid=${wksht.getSheetId()}`
}

function summaryInfo(sheet, wksht, row) {
  name = wksht.getSheetName();
  [[count], [points]] = wksht.getRange('S2:S3').getValues();
  [fraction, percent] = count.split(' ');
  [correct, total]    = fraction.split('/').map(x => parseInt(x));

  var url = getSheetUrl(wksht);
  sheet.getRange(`K${row}`).setFormula(`=hyperlink("${url}", "${name}")`);
  
  sheet.getRange(`M${row}`).setFormula(`=${correct}/${total}`);
  sheet.getRange(`M${row}`).setNumberFormat(`#?/${total}`);
  
  sheet.getRange(`O${row}`).setValue(points);
  SpreadsheetApp.flush();
};

function onEdit(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet();
  if (sheet.getSheetName() == 'Summary') {
    var wkshts = sheet.getSheets();
    var row = 75;
    
    wkshts.forEach((wksht) => {
      name = wksht.getSheetName();
      if (!['Summary','Template'].includes(name)) {
        wksht.getRange('S2:S3').clearContent();
        /*
        wksht.getRange('G2:S3').clearContent();
        wksht.getRange('G2').setFormula('=roundOf64Correct()');
        wksht.getRange('I2').setFormula('=roundOf32Correct()');
        wksht.getRange('K2').setFormula('=sweet16Correct()');
        wksht.getRange('M2').setFormula('=elite8Correct()');
        wksht.getRange('O2').setFormula('=final4Correct()');
        wksht.getRange('Q2').setFormula('=championshipCorrect()');
        wksht.getRange('S2').setFormula('=totalCorrect()');
        */
        wksht.getRange('G2:G3').setValues(roundOf64Correct(wksht).map(x => [x]));
        wksht.getRange('I2:I3').setValues(roundOf32Correct(wksht).map(x => [x]));
        wksht.getRange('K2:K3').setValues(sweet16Correct(wksht).map(x => [x]));
        wksht.getRange('M2:M3').setValues(elite8Correct(wksht).map(x => [x]));
        wksht.getRange('O2:O3').setValues(final4Correct(wksht).map(x => [x]));
        wksht.getRange('Q2:Q3').setValues(championshipCorrect(wksht).map(x => [x]));
        wksht.getRange('S2:S3').setValues(totalCorrect(wksht).map(x => [x]));
        
        SpreadsheetApp.flush();
        summaryInfo(sheet, wksht, row);
        row = row + 1;
      };
    });
    SpreadsheetApp.flush();
  }
};
