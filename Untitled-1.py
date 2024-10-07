// © sbtnc
// Created: 2024-03-10
// Last modified: 2024-03-10
// Version 1.0

// @version=5

indicator("Multi-Timeframe Separators", "MTF Separators [year, month, dayofmonth...]", overlay = true, max_lines_count = 500)



//--------------------------------------------------------------------
//#region                      Constants
//--------------------------------------------------------------------

color   COLOR_1 = color.green
color   COLOR_2 = color.orange
color   COLOR_3 = color.red
color   COLOR_4 = color.blue

//#endregion


//--------------------------------------------------------------------
//#region                        Inputs
//--------------------------------------------------------------------

opt1  = "5S"
opt2  = "10S"
opt3  = "15S"
opt4  = "30S"
opt5  = "1"
opt6  = "2"
opt7  = "3"
opt8  = "5"
opt9  = "10"
opt10 = "15"
opt11 = "30"
opt12 = "45"
opt13 = "60"
opt14 = "120"
opt15 = "180"
opt16 = "240"
opt17 = "360"
opt18 = "480"
opt19 = "720"
opt20 = "1D"
opt21 = "1W"
opt22 = "1M"
opt23 = "3M"
opt24 = "6M"
opt25 = "12M"

g1 = "Separators"

enableSeparatorInput1       = input.bool    (true,      "",             group = g1, inline = "#1")
separatorTimeframeInput1    = input.string  ("1D",      "",             group = g1, inline = "#1", options = [opt1, opt2, opt3, opt4, opt5, opt6, opt7, opt8, opt9, opt10, opt11, opt12, opt13, opt14, opt15, opt16, opt17, opt18, opt19, opt20, opt21, opt22, opt23, opt24, opt25])
separatorLookbackInput1     = input.int     (500,       "",             group = g1, inline = "#1", minval = 1, maxval = 500, display = display.none)
enableSeparatorInput2       = input.bool    (true,      "",             group = g1, inline = "#2")
separatorTimeframeInput2    = input.string  ("1W",      "",             group = g1, inline = "#2", options = [opt1, opt2, opt3, opt4, opt5, opt6, opt7, opt8, opt9, opt10, opt11, opt12, opt13, opt14, opt15, opt16, opt17, opt18, opt19, opt20, opt21, opt22, opt23, opt24, opt25])
separatorLookbackInput2     = input.int     (500,       "",             group = g1, inline = "#2", minval = 1, maxval = 500, display = display.none)
enableSeparatorInput3       = input.bool    (true,      "",             group = g1, inline = "#3")
separatorTimeframeInput3    = input.string  ("1M",      "",             group = g1, inline = "#3", options = [opt1, opt2, opt3, opt4, opt5, opt6, opt7, opt8, opt9, opt10, opt11, opt12, opt13, opt14, opt15, opt16, opt17, opt18, opt19, opt20, opt21, opt22, opt23, opt24, opt25])
separatorLookbackInput3     = input.int     (500,       "",             group = g1, inline = "#3", minval = 1, maxval = 500, display = display.none)
enableSeparatorInput4       = input.bool    (false,     "",             group = g1, inline = "#4")
separatorTimeframeInput4    = input.string  ("12M",     "",             group = g1, inline = "#4", options = [opt1, opt2, opt3, opt4, opt5, opt6, opt7, opt8, opt9, opt10, opt11, opt12, opt13, opt14, opt15, opt16, opt17, opt18, opt19, opt20, opt21, opt22, opt23, opt24, opt25])
separatorLookbackInput4     = input.int     (500,       "",             group = g1, inline = "#4", minval = 1, maxval = 500, display = display.none)

g2 = "Style"

separatorColorInput1        = input.color   (COLOR_1,   "",             group = g2, inline = "#1")
separatorWidthInput1        = input.int     (1,         "",             group = g2, inline = "#1", minval = 1, display = display.none)
separatorStyleInput1        = input.string  ("Dotted",  "",             group = g2, inline = "#1", options =["Solid", "Dashed", "Dotted"], display = display.none)
separatorColorInput2        = input.color   (COLOR_2,   "",             group = g2, inline = "#2")
separatorWidthInput2        = input.int     (1,         "",             group = g2, inline = "#2", minval = 1, display = display.none)
separatorStyleInput2        = input.string  ("Solid",   "",             group = g2, inline = "#2", options =["Solid", "Dashed", "Dotted"], display = display.none)
separatorColorInput3        = input.color   (COLOR_3,   "",             group = g2, inline = "#3")
separatorWidthInput3        = input.int     (2,         "",             group = g2, inline = "#3", minval = 1, display = display.none)
separatorStyleInput3        = input.string  ("Solid",   "",             group = g2, inline = "#3", options =["Solid", "Dashed", "Dotted"], display = display.none)
separatorColorInput4        = input.color   (COLOR_4,   "",             group = g2, inline = "#4")
separatorWidthInput4        = input.int     (3,         "",             group = g2, inline = "#4", minval = 1, display = display.none)
separatorStyleInput4        = input.string  ("Solid",   "",             group = g2, inline = "#4", options =["Solid", "Dashed", "Dotted"], display = display.none)

g3 = "Preferences"

showNextSeparatorInput      = input.bool    (false,     "Show Next",    group = g3)

//#endregion


//--------------------------------------------------------------------
//#region                         Types 
//--------------------------------------------------------------------
//#endregion




//--------------------------------------------------------------------
//#region                   Functions & methods
//--------------------------------------------------------------------

// @function    Get the value at the last index of the given `array series` on the previous bar
// @returns     The preceding last value
getLast(arr) =>
    // @variable The preceding `array serie`
    _prevThis = arr[1]
    
    switch
        na(_prevThis) => na // Array is undefined on the first bar
        _prevThis.size() == 0 => na // Array is empty
        => _prevThis.last()


// @funcion Get the line style from a given input setting
// @returns const string
getLineStyle(string input) =>
    var _style = switch input
        "Solid"     => line.style_solid
        "Dotted"    => line.style_dotted
        "Dashed"    => line.style_dashed


yearChange(array<int> intraTimeArray) =>
    bool _changed = false
    int _prevTime = getLast(intraTimeArray)
    for _time in intraTimeArray
        if year(_prevTime) != year(_time)
            _changed := true
            log.info("\n Change at {0}", str.format_time(_time))
            break
        _prevTime := _time
    _changed


monthChange(array<int> intraTimeArray) =>
    bool _changed = false
    int _prevTime = getLast(intraTimeArray)
    for _time in intraTimeArray
        if month(_prevTime) != month(_time)
            _changed := true
            log.info("\n Change at {0}", str.format_time(_time))
            break
        _prevTime := _time
    _changed


weekChange(array<int> intraTimeArray) =>
    bool _changed = false
    int _prevTime = getLast(intraTimeArray)
    for _time in intraTimeArray
        if weekofyear(_prevTime) != weekofyear(_time)
            _changed := true
            log.info("\n Change at {0}", str.format_time(_time))
            break
        _prevTime := _time
    _changed


dayChange(array<int> intraTimeArray) =>
    bool _changed = false
    int _prevTime = getLast(intraTimeArray)
    for _time in intraTimeArray
        if dayofmonth(_prevTime) != dayofmonth(_time)
            _changed := true
            log.info("\n Change at {0}", str.format_time(_time))
            break
        _prevTime := _time
    _changed 
 

hourChange(array<int> intraTimeArray) =>
    bool _changed = false
    int _prevTime = getLast(intraTimeArray)
    for _time in intraTimeArray
        if hour(_prevTime) != hour(_time)
            _changed := true
            log.info("\n Change at {0}", str.format_time(_time))
            break
        _prevTime := _time
    _changed


minuteChange() =>
    minute[1] != minute


monthChange(array<int> intraTimeArray, int multiplier) =>
    var _count = 0
    var _monthArray = array.new_int()

    // Populate with hours
    if barstate.isfirst
        for i = 0 to 12 / multiplier -1
            _monthArray.push(i * multiplier +1)
        log.info("\n Months list {0}", _monthArray)

    bool _changed = false
    int _prevTime = getLast(intraTimeArray)
    for _time in intraTimeArray
        // Change to an hour in hour list
        //if month[1] != month and _monthArray.includes(month)
        if month(_prevTime) != month(_time) and _monthArray.includes(month(_time))
            _changed := true
            break
        _prevTime := _time
    _changed


hourChange(array<int> intraTimeArray, int multiplier) =>
    var _count = 0
    var _hourArray = array.new_int()

    // Populate with hours
    if barstate.isfirst
        for i = 0 to 24 / multiplier -1
            _hourArray.push(i * multiplier)
        log.info("\n Hours list {0}", _hourArray)

    bool _changed = false
    int _prevTime = getLast(intraTimeArray)
    for _time in intraTimeArray
        // Change to an hour in hour list
        if hour(_prevTime) != hour(_time) and _hourArray.includes(hour(_time))
            _changed := true
            //log.info("\n Change at {0}", str.format_time(_time))
            break
        _prevTime := _time
    _changed


// - 45 minutes interval does not start at 00:00
//   > start counting from 00:00 
//   > remove 45 minute from supported list
// - 45 minutes interval and 30 minutes timeframe -> odd need to implement ltf
minuteChange(int multiplier) =>
    var int _last = na
    int increment = multiplier * 60 * 1000

    // At the bar change
    if time % increment == 0
        _last := time
        log.info("At {0}", str.format_time(_last))

    // Some bars were missing
    else if time - _last >= increment
        _last := time - time % increment
        //log.warning("Past {0} by {1}s", str.format_time(_last), (time % increment) / 1000)
    
    else 
        log.error("{0}m", (time - _last) / 1000 / 60)

    ta.change(_last)


secondChange(int multiplier) =>
    var int _last = na
    int increment = multiplier * 1000

    // At the bar change
    if time % increment == 0
        _last := time
        log.info("At {0}", str.format_time(_last))

    // Some bars were missing
    else if time - _last >= increment
        _last := time - time % increment
        //log.warning("Past {0} by {1}s", str.format_time(_last), (time % increment) / 1000)

    ta.change(_last)


timeChange(ltfTimeArray, string timeframe) =>
    switch timeframe
        "5S"  => secondChange(5)
        "10S" => secondChange(10)
        "15S" => secondChange(15)
        "30S" => secondChange(30)
        "1"   => minuteChange()
        "2"   => minuteChange(2)
        "3"   => minuteChange(3)
        "5"   => minuteChange(5)
        "10"  => minuteChange(10)
        "15"  => minuteChange(15)
        "30"  => minuteChange(30)
        "45"  => minuteChange(45)
        "60"  => hourChange(ltfTimeArray)
        "120" => hourChange(ltfTimeArray, 2)
        "180" => hourChange(ltfTimeArray, 3)
        "240" => hourChange(ltfTimeArray, 4)
        "360" => hourChange(ltfTimeArray, 6)
        "480" => hourChange(ltfTimeArray, 8)
        "720" => hourChange(ltfTimeArray, 12)
        "1D"  => dayChange(ltfTimeArray)
        "1W"  => weekChange(ltfTimeArray)
        "1M"  => monthChange(ltfTimeArray)
        "3M"  => monthChange(ltfTimeArray, 3)
        "6M"  => monthChange(ltfTimeArray, 6)
        "12M" => yearChange(ltfTimeArray)

drawSeparator(ltfTimeArray, bool isEnabled, string tf, color color, int width, string style, int lookback) =>
    var lineArray = array.new_line()
    _canDisplayOnChartTimeframe = timeframe.in_seconds(tf) > timeframe.in_seconds()

    if isEnabled and _canDisplayOnChartTimeframe
        if timeChange(ltfTimeArray, tf)
            // y1 and y2 should not be equal prices otherwise draw vertical lines
            lineArray.push(
                 line.new(time, open, time, open + syminfo.mintick, xloc.bar_time, extend.both, color, getLineStyle(style), width)
                 )


            if lineArray.size() > lookback
                line.delete(lineArray.shift())

//          // Projection
//          if showNextSeparatorInput
//              var line projectionLine = line.new(na, na, na, na, xloc.bar_time, extend.both, color, getLineStyle(style), width)
//  
//              nextTime = time + timeframe.in_seconds(tf) * 1000
//              log.info("\n {0}", timeframe.in_seconds(tf))
//              log.info(
//                   "\n time {0}" +
//                   "\n next time {1}",
//                   str.format_time(time),
//                   str.format_time(nextTime)
//                   )
//              projectionLine.set_xy1(nextTime, open)
//              projectionLine.set_xy2(nextTime, syminfo.mintick)

//#endregion


//--------------------------------------------------------------------
//#region                 Variables declarations
//--------------------------------------------------------------------
//#endregion


//--------------------------------------------------------------------
//#region                         Logic
//--------------------------------------------------------------------

// Can find a generic rules based on module % ? then find lowest shared increment
// -- chart timeframe 45-minute, 1-week
// -- indicator timeframe

ltf = timeframe.period

pgcd(simple int a, simple int b) =>
    int _a = a
    int _tempA = na
    int _b = b
    int _tempB = na

    while (_a % _b) != 0
        log.info("a: {0}", _a)
        log.info("b: {0}", _b)
        log.info("a % b = {0}", _a % _b)

        if (_a % _b ) != 0
            _tempA := _a
            _a := _b
            _b := _tempA % _b

    log.info("-> b: {0}", _b)
    simple int _res = _b
    _res

//res = pgcd(timeframe.in_seconds(separatorTimeframeInput1) / 1000, timeframe.in_seconds() / 1000)


//if barstate.islast
//    //res = pgcd(60, 45) // 7200 3600
//    res = pgcd(timeframe.in_seconds(separatorTimeframeInput1), timeframe.in_seconds())
//    
//    if timeframe.in_seconds(separatorTimeframeInput1) % timeframe.in_seconds() != 0
//        log.error("timeframe is odd, need fix")

_chartTfInSec = timeframe.in_seconds()
_separatorTfInSec = timeframe.in_seconds(separatorTimeframeInput1)
var simple int _pgcd = pgcd(_chartTfInSec, _separatorTfInSec)

if barstate.isfirst
    if _chartTfInSec % _separatorTfInSec != 0
        simple string _ltf = timeframe.from_seconds(_pgcd)
        log.info("PGCD {0}", _ltf)

    //if separatorTimeframeInput1 == "60"
    //    ltf := switch
    //        timeframe.in_seconds() == timeframe.in_seconds("45") => "15"
        
//else if separatorTimeframeInput1 == "120"
//    ltf := switch
//        timeframe.in_seconds() == timeframe.in_seconds("45") => "15"
//
//else if separatorTimeframeInput1 == "240"
//    ltf := switch
//        timeframe.in_seconds() == timeframe.in_seconds("45") => "15"
//
//else if separatorTimeframeInput1 == "1W"
//    ltf := switch 
//        timeframe.in_seconds() >= timeframe.in_seconds("1D") => "720"
//        timeframe.in_seconds() >= timeframe.in_seconds("60") => "60"
//
//else if separatorTimeframeInput1 == "1M"
//    ltf := switch 
//        timeframe.in_seconds() >= timeframe.in_seconds("1D") => "360"
//
//else if separatorTimeframeInput1 == "3M"
//    ltf := switch 
//        timeframe.in_seconds() >= timeframe.in_seconds("1D") => "360"
//
//else if separatorTimeframeInput1 == "6M"
//    ltf := switch 
//        timeframe.in_seconds() >= timeframe.in_seconds("1D") => "360"
//
//else if separatorTimeframeInput1 == "12M"
//    ltf := switch
//        timeframe.in_seconds() >= timeframe.in_seconds("1W") => "1D"


ltfTimeArray = request.security_lower_tf(syminfo.tickerid, ltf, time)

if barstate.islastconfirmedhistory
    log.info("data size in bar {0}", ltfTimeArray.size())

//#endregion


//--------------------------------------------------------------------
//#region                        Visuals
//--------------------------------------------------------------------

drawSeparator(ltfTimeArray, enableSeparatorInput1, separatorTimeframeInput1, separatorColorInput1, separatorWidthInput1, separatorStyleInput1, separatorLookbackInput1)
drawSeparator(ltfTimeArray, enableSeparatorInput2, separatorTimeframeInput2, separatorColorInput2, separatorWidthInput2, separatorStyleInput2, separatorLookbackInput2)
drawSeparator(ltfTimeArray, enableSeparatorInput3, separatorTimeframeInput3, separatorColorInput3, separatorWidthInput3, separatorStyleInput3, separatorLookbackInput3)
drawSeparator(ltfTimeArray, enableSeparatorInput4, separatorTimeframeInput4, separatorColorInput4, separatorWidthInput4, separatorStyleInput4, separatorLookbackInput4)

//#endregion


//--------------------------------------------------------------------
//#region                         Alerts
//--------------------------------------------------------------------
//#endregion


//--------------------------------------------------------------------
//#region                         Debug
//--------------------------------------------------------------------

// Table

if barstate.islast
    var table t = table.new(position.bottom_right, 3, 2)

    t.cell(0, 0, "Chart", text_color = chart.fg_color)
    t.cell(1, 0, "Separator", text_color = chart.fg_color)
    t.cell(2, 0, "Intrabar", text_color = chart.fg_color)

    t.cell(0, 1, timeframe.period, text_color = chart.fg_color)
    t.cell(1, 1, separatorTimeframeInput1, text_color = chart.fg_color)
    t.cell(2, 1, ltf, text_color = chart.fg_color)

//#endregion


//--------------------------------------------------------------------
//#region                      Performances
//--------------------------------------------------------------------
//#endregion