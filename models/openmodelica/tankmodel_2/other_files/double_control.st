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
  END_VAR
  VAR_OUTPUT
    controll : REAL;
  END_VAR

  IF (VALORE<1.015) THEN
    controll := 0.0;
  ELSIF (controll = 0.0 and VALORE<2.4) THEN
    controll := 0.0;
  ELSIF (controll = 0.0 and VALORE>2.4) THEN
    controll := 1.0;
  ELSIF (controll =1.0 and VALORE<2.4) THEN
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

PROGRAM pressure
  VAR
    WORD1 AT %IW100 : UINT;
    WORD2 AT %IW101 : UINT;
    WORD3 AT %MD0 : REAL;
    prova1 AT %QW100 : UINT;
    prova2 AT %QW101 : UINT;
  END_VAR
  VAR
    control0 : control;
    function18_OUT : BOOL;
    function18_WORDSTOREAL : REAL;
    prova9_OUT : BOOL;
    prova9_LOWW : UINT;
    prova9_HIGG : UINT;
  END_VAR

  function18_OUT := function1(LOWWORD := WORD2, HIGHWORD := WORD1, WORDSTOREAL => function18_WORDSTOREAL);
  WORD3 := function18_WORDSTOREAL;
  control0(VALORE := function18_WORDSTOREAL);
  prova9_OUT := prova(INPP := control0.controll, LOWW => prova9_LOWW, HIGG => prova9_HIGG);
  prova2 := prova9_LOWW;
  prova1 := prova9_HIGG;
END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : pressure;
  END_RESOURCE
END_CONFIGURATION
