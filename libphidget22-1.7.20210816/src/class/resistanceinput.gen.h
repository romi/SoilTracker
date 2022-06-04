#ifndef _RESISTANCEINPUT_H_
#define _RESISTANCEINPUT_H_

/* Generated by WriteClassHeaderVisitor: Mon Aug 16 2021 13:12:04 GMT-0600 (Mountain Daylight Time) */

typedef struct _PhidgetResistanceInput *PhidgetResistanceInputHandle;

/* Methods */
API_PRETURN_HDR PhidgetResistanceInput_create(PhidgetResistanceInputHandle *ch);
API_PRETURN_HDR PhidgetResistanceInput_delete(PhidgetResistanceInputHandle *ch);

/* Properties */
API_PRETURN_HDR PhidgetResistanceInput_setDataInterval(PhidgetResistanceInputHandle ch,
  uint32_t dataInterval);
API_PRETURN_HDR PhidgetResistanceInput_getDataInterval(PhidgetResistanceInputHandle ch,
  uint32_t *dataInterval);
API_PRETURN_HDR PhidgetResistanceInput_getMinDataInterval(PhidgetResistanceInputHandle ch,
  uint32_t *minDataInterval);
API_PRETURN_HDR PhidgetResistanceInput_getMaxDataInterval(PhidgetResistanceInputHandle ch,
  uint32_t *maxDataInterval);
API_PRETURN_HDR PhidgetResistanceInput_getResistance(PhidgetResistanceInputHandle ch,
  double *resistance);
API_PRETURN_HDR PhidgetResistanceInput_getMinResistance(PhidgetResistanceInputHandle ch,
  double *minResistance);
API_PRETURN_HDR PhidgetResistanceInput_getMaxResistance(PhidgetResistanceInputHandle ch,
  double *maxResistance);
API_PRETURN_HDR PhidgetResistanceInput_setResistanceChangeTrigger(PhidgetResistanceInputHandle ch,
  double resistanceChangeTrigger);
API_PRETURN_HDR PhidgetResistanceInput_getResistanceChangeTrigger(PhidgetResistanceInputHandle ch,
  double *resistanceChangeTrigger);
API_PRETURN_HDR PhidgetResistanceInput_getMinResistanceChangeTrigger(PhidgetResistanceInputHandle ch,
  double *minResistanceChangeTrigger);
API_PRETURN_HDR PhidgetResistanceInput_getMaxResistanceChangeTrigger(PhidgetResistanceInputHandle ch,
  double *maxResistanceChangeTrigger);
API_PRETURN_HDR PhidgetResistanceInput_setRTDWireSetup(PhidgetResistanceInputHandle ch,
  Phidget_RTDWireSetup RTDWireSetup);
API_PRETURN_HDR PhidgetResistanceInput_getRTDWireSetup(PhidgetResistanceInputHandle ch,
  Phidget_RTDWireSetup *RTDWireSetup);

/* Events */
typedef void (CCONV *PhidgetResistanceInput_OnResistanceChangeCallback)(PhidgetResistanceInputHandle ch,
  void *ctx, double resistance);

API_PRETURN_HDR PhidgetResistanceInput_setOnResistanceChangeHandler(PhidgetResistanceInputHandle ch,
  PhidgetResistanceInput_OnResistanceChangeCallback fptr, void *ctx);

#endif /* _RESISTANCEINPUT_H_ */
