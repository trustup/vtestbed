FUNCTION_BLOCK control
  VAR_INPUT
    xi821bx : REAL;
    restart : REAL;
  END_VAR
  VAR_OUTPUT
    on_off : REAL := 1.0;
    reset : REAL;
  END_VAR

  IF (restart = 0.0 and on_off = 1.0 and xi821bx < 140.0) THEN
      on_off := 1.0;
    ELSIF (restart = 0.0 and on_off = 1.0 and xi821bx > 140.0) THEN
      on_off := 0.0;
    ELSIF (restart = 0.0 and on_off = 0.0 and xi821bx < 140.0) THEN
      on_off := 0.0;
    ELSIF (restart = 1.0 and on_off = 0.0 and xi821bx < 140.0) THEN
      on_off := 1.0;
      reset := 0.0;
    END_IF; 
END_FUNCTION_BLOCK

FUNCTION words2real : BOOL
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

FUNCTION real2words : BOOL
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

PROGRAM steam_turbine
  VAR
    sensor_821bx_1 AT %IW100 : UINT;
    sensor_821bx_2 AT %IW101 : UINT;
    WORD3 AT %MD0 : REAL;
    WORD4 AT %IW102 : UINT;
    WORD5 AT %IW103 : UINT;
    WORD6 AT %MD3 : REAL;
    plc_821_1 AT %QW100 : UINT;
    plc_821_2 AT %QW101 : UINT;
    plc_821_3 AT %QW102 : UINT;
    plc_821_4 AT %QW103 : UINT;
  END_VAR
  VAR
    control0 : control;
    words2real8_OUT : BOOL;
    words2real8_WORDSTOREAL : REAL;
    words2real14_OUT : BOOL;
    words2real14_WORDSTOREAL : REAL;
    real2words9_OUT : BOOL;
    real2words9_LOWW : UINT;
    real2words9_HIGG : UINT;
    real2words18_OUT : BOOL;
    real2words18_LOWW : UINT;
    real2words18_HIGG : UINT;
  END_VAR

  words2real8_OUT := words2real(LOWWORD := sensor_821bx_2, HIGHWORD := sensor_821bx_1, WORDSTOREAL => words2real8_WORDSTOREAL);
  WORD3 := words2real8_WORDSTOREAL;
  words2real14_OUT := words2real(LOWWORD := WORD5, HIGHWORD := WORD4, WORDSTOREAL => words2real14_WORDSTOREAL);
  control0(xi821bx := words2real8_WORDSTOREAL, restart := words2real14_WORDSTOREAL);
  real2words9_OUT := real2words(INPP := control0.on_off, LOWW => real2words9_LOWW, HIGG => real2words9_HIGG);
  plc_821_2 := real2words9_LOWW;
  plc_821_1 := real2words9_HIGG;
  real2words18_OUT := real2words(INPP := control0.reset, LOWW => real2words18_LOWW, HIGG => real2words18_HIGG);
  plc_821_4 := real2words18_LOWW;
  plc_821_3 := real2words18_HIGG;
  WORD6 := words2real14_WORDSTOREAL;
END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : steam_turbine;
  END_RESOURCE
END_CONFIGURATION
