FUNCTION function1 : BOOL
  VAR_INPUT
    LOWWORD : UINT;
    HIGHWORD : UINT;
  END_VAR
  VAR_OUTPUT
    WORDSTOREAL : REAL;
  END_VAR

  {{
  union words_to_real {
  uint16_t i[2];
  float f;
  }w2r;
  w2r.i[0] = LOWWORD;
  w2r.i[1] = HIGHWORD;
  WORDSTOREAL = w2r.f;
  }}
END_FUNCTION

FUNCTION_BLOCK control
  VAR_INPUT
    VALORE : REAL;
    VALORE2 : REAL;
  END_VAR
  VAR_OUTPUT
    controll : REAL;
  END_VAR

  IF (VALORE = 0.0 and VALORE2 = 0.0) THEN
    controll := 1.0;
  ELSIF (VALORE = 0.0 and VALORE2 = 1.0) THEN
    controll := 0.0;
  ELSIF (VALORE = 1.0 and VALORE2 = 1.0) THEN
    controll := 1.0;
  ELSIF (VALORE = 0.0 and VALORE2 = 2.0) THEN
    controll := 0.0;
  ELSIF (VALORE = 1.0 and VALORE2 = 2.0) THEN
    controll := 1.0;
  END_IF; 
END_FUNCTION_BLOCK

FUNCTION prova : BOOL
  VAR_INPUT
    INPP : REAL;
  END_VAR
  VAR_OUTPUT
    LOWW : UINT;
    HIGG : UINT;
  END_VAR

  {{
  union real_to_words {
  uint16_t i[2];
  float f;
  }r2w;
  r2w.f = INPP;
  LOWW = r2w.i[0];
  HIGG = r2w.i[1];
  }}
END_FUNCTION

PROGRAM robot
  VAR
    STATE_STATION_w1 AT %IW100 : UINT;
    STATION_w1 AT %IW102 : UINT;
    STATION_w2 AT %IW103 : UINT;
    STATE_STATION_w2 AT %IW101 : UINT;
    WORD3 AT %MD0 : REAL;
    WORD6 AT %MD1 : REAL;
    ROBOT_STATE_w1 AT %QW100 : UINT;
    ROBOT_STATE_w2 AT %QW101 : UINT;
  END_VAR
  VAR
    control0 : control;
    function18_OUT : BOOL;
    function18_WORDSTOREAL : REAL;
    function116_OUT : BOOL;
    function116_WORDSTOREAL : REAL;
    prova9_OUT : BOOL;
    prova9_LOWW : UINT;
    prova9_HIGG : UINT;
  END_VAR

  function18_OUT := function1(LOWWORD := STATE_STATION_w2, HIGHWORD := STATE_STATION_w1, WORDSTOREAL => function18_WORDSTOREAL);
  WORD3 := function18_WORDSTOREAL;
  function116_OUT := function1(LOWWORD := STATION_w2, HIGHWORD := STATION_w1, WORDSTOREAL => function116_WORDSTOREAL);
  control0(VALORE := function18_WORDSTOREAL, VALORE2 := function116_WORDSTOREAL);
  prova9_OUT := prova(INPP := control0.controll, LOWW => prova9_LOWW, HIGG => prova9_HIGG);
  ROBOT_STATE_w2 := prova9_LOWW;
  ROBOT_STATE_w1 := prova9_HIGG;
  WORD6 := function116_WORDSTOREAL;
END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : robot;
  END_RESOURCE
END_CONFIGURATION
