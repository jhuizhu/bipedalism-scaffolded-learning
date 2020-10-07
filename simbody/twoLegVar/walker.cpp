#include "Simbody.h"
#include "armadillo"
#include <math.h>
#include <stdio.h>
#include <iostream>
#include <exception>
using namespace SimTK;
using namespace arma;
using namespace std;

#ifdef VIS_ON
static const int RunMenuId = 3, HelpMenuId = 7;
static const int GoItem = 1, ReplayItem=2, QuitItem=3;
Array_<State> saveEm;
#endif

int main(int argc, char* argv[]) { 
  //for (int i = 1; i < 13; ++i) {
  //printf ("Argument %d: %f\n", i, atof(argv[i]));
  //}
  /************** System set up ***************/
  bool visOn               = true;
  bool controller          = true;
  bool stateAdvance        = false;
  float halfBodyX          = atof(argv[1]);
  float halfBodyY          = atof(argv[2]);
  float halfBodyZ          = atof(argv[3]);
  float halfFootBodyX      = atof(argv[4]);
  float halfFootBodyY      = atof(argv[5]);
  float halfFootBodyZ      = atof(argv[6]);
  float k1                 = atof(argv[7]);
  float k2                 = atof(argv[8]);
  float lambda1            = atof(argv[9]);
  float lambda2            = atof(argv[10]);
  float bodyStraightK      = atof(argv[11]);
  float bodyStraightLambda = atof(argv[12]);
  float kneeMass           = atof(argv[13]);
  float ankleMass          = atof(argv[14]);
  float hipMass            = atof(argv[15]);
  float stepK              = atof(argv[16]);
  float stableTolerance    = atof(argv[17]);
  float tibiaLength        = atof(argv[18]);
  float femurLength        = atof(argv[19]);
  float standOffset        = atof(argv[20]);/*0.05;*/
  float stepOffset         = atof(argv[21]);/*-0.15;*/
  const float speed        = .0;
  const Real fFac          = 0.3;
  const Real fDis          = 1;
  const Real fVis          = 0.3;
  const Real fK            = 1e+8;
  const Real MaxStepSize   = Real(1/30.); // 33 1/3 ms (30 Hz)
  const int  DrawEveryN    = 1;           // 33 1/3 ms frame update (30 Hz)
  const float simTime      = 15;
  MultibodySystem system;
  SimbodyMatterSubsystem matter(system);
  GeneralForceSubsystem forces(system);
  Force::UniformGravity gravity(forces, matter, Vec3(0, -9.81, 0));
  ContactTrackerSubsystem  tracker(system);
  CompliantContactSubsystem contactForces(system, tracker);
  contactForces.setTrackDissipatedEnergy(true);
  contactForces.setTransitionVelocity(1e-3);
  GeneralContactSubsystem OLDcontact(system);
  /************** System set up ***************/


  /************** Body ***************/
  Vec3 halfSize(halfBodyX,halfBodyY,halfBodyZ);
  ContactGeometry::TriangleMesh body(PolygonalMesh::createBrickMesh(halfSize, 6));
#ifdef VIS_ON
  DecorativeMesh showBody(body.createPolygonalMesh());
#endif
  const Real bodyMass = halfSize[0] * halfSize[1] * halfSize[2] * 8 * 1180;
  Body::Rigid bodyBody(MassProperties(bodyMass, Vec3(0), bodyMass *  UnitInertia::brick(halfSize)));
#ifdef VIS_ON
  bodyBody.addDecoration(Transform(), showBody.setColor(Purple).setOpacity(1));
  bodyBody.addDecoration(Transform(), showBody.setColor(Black).setRepresentation(DecorativeGeometry::DrawWireframe));
#endif
  bodyBody.addContactSurface(Transform(), ContactSurface(body, ContactMaterial(fK, fDis, fFac, fFac, fVis), .5 /*thickness*/));
  MobilizedBody::Free bodyMBody(matter.Ground(), Transform(Vec3(0,tibiaLength+femurLength+halfFootBodyY+halfBodyY,0)), bodyBody, Transform(Vec3(0)));
  /************** Body ***************/

  /************** Foot ***************/
  Vec3 halfSizeFoot(halfFootBodyX,halfFootBodyY,halfFootBodyZ);
  ContactGeometry::TriangleMesh foot(PolygonalMesh::createBrickMesh(halfSizeFoot, 6));
#ifdef VIS_ON
  DecorativeMesh showFoot(foot.createPolygonalMesh());
#endif
  const Real footMass = halfSizeFoot[0] * halfSizeFoot[1] * halfSizeFoot[2] * 8 * 1180;
  Body::Rigid footBody(MassProperties(footMass, Vec3(0), footMass * UnitInertia::brick(halfSizeFoot)));
#ifdef VIS_ON
  footBody.addDecoration(Transform(), showFoot.setColor(Red).setOpacity(1));
  footBody.addDecoration(Transform(), showFoot.setColor(Gray).setRepresentation(DecorativeGeometry::DrawWireframe));
#endif
  footBody.addContactSurface(Transform(), ContactSurface(foot, ContactMaterial(fK, fDis, fFac, fFac, fVis), .5 /*thickness*/));
  MobilizedBody::Free footMobodRight (matter.Ground(), Transform(Vec3(0,halfFootBodyY,-0.25)), footBody, Transform(Vec3(0)));
  MobilizedBody::Free footMobodLeft (matter.Ground(), Transform(Vec3(0,halfFootBodyY,0.25)), footBody, Transform(Vec3(0)));
  /************** Foot ***************/

  /************** Ground ***************/
  const Rotation R_xdown(-Pi/2,ZAxis);
  matter.Ground().updBody().addContactSurface(
      Transform(R_xdown, Vec3(0,0,0)),ContactSurface(ContactGeometry::HalfSpace(), ContactMaterial(fK,fDis,fFac,fFac,fVis)));
  /************** Ground ***************/

  /************** RightLeg ***************/
  Body::Rigid knee(MassProperties(kneeMass, Vec3(0), UnitInertia::sphere(0.05)));
  Body::Rigid ankle(MassProperties(ankleMass, Vec3(0), footMass * (UnitInertia::brick(halfSizeFoot))));
  Body::Rigid hip(MassProperties(hipMass, Vec3(0), bodyMass * UnitInertia::brick(halfSize).shiftFromCentroid(Vec3(0, halfBodyY, 0))));
#ifdef VIS_ON
  DecorativeSphere bigSphere (0.05);
  DecorativeSphere smallSphere (0.05);
  smallSphere.setColor (Vec3 (0.5, 0.9, 0));
  bigSphere.setColor (Vec3 (0.5, 0.9, 0.9));
  knee.addDecoration(Transform(), bigSphere);
  ankle.addDecoration(Transform(), smallSphere);
#endif
  knee.addContactSurface(Transform(), ContactSurface(ContactGeometry::Sphere(0.1), ContactMaterial(fK, fDis, fFac, fVis)));
  MobilizedBody::Pin rightAnklePin(footMobodRight, Transform(Vec3(0, 0, 0)), ankle, Transform(Vec3(0)));
  MobilizedBody::Pin rightTibia(rightAnklePin, Transform(Vec3(0, tibiaLength, 0)), knee, Transform(Vec3(0)));
  MobilizedBody::Pin rightFemur(rightTibia, Transform(Vec3(0, femurLength, 0)), hip, Transform(Vec3(0, 0, 0)));
#ifdef VIS_ON
  rightAnklePin.addBodyDecoration (Vec3(0,tibiaLength/2,0), DecorativeCylinder(0.03, tibiaLength/2).setColor(Black));
  rightTibia.addBodyDecoration (Vec3(0,femurLength/2,0), DecorativeCylinder(0.03, femurLength/2).setColor(Black));     
#endif
  rightTibia.setDefaultAngle (Pi/10);
  /************** RightLeg ***************/

  /************** LeftLeg ***************/
  MobilizedBody::Pin leftAnklePin(footMobodLeft, Transform(Vec3(0, 0, 0)), ankle, Transform(Vec3(0)));
  MobilizedBody::Pin leftTibia(leftAnklePin, Transform(Vec3(0, tibiaLength, 0)), knee, Transform(Vec3(0)));
  MobilizedBody::Pin leftFemur(leftTibia, Transform(Vec3(0, femurLength, 0)), hip, Transform(Vec3(0, 0, 0)));
#ifdef VIS_ON
  leftAnklePin.addBodyDecoration (Vec3(0,tibiaLength/2,0), DecorativeCylinder(0.03, tibiaLength/2).setColor(Black));
  leftTibia.addBodyDecoration (Vec3(0,femurLength/2,0), DecorativeCylinder(0.03, femurLength/2).setColor(Black));     
#endif
  Constraint::Weld leftFootConstraint (footMobodLeft, Vec3(0, -halfFootBodyY+0.002, 0), matter.Ground(), Vec3(0, 0, 0.25));
  Constraint::Weld rightFootConstraint (footMobodRight, Vec3(0, -halfFootBodyY+0.002, 0), matter.Ground(), Vec3(0, 0, -0.25));
  Constraint::Weld leftHipConstraint (bodyMBody, Vec3(0, -halfBodyY, 0.25), leftFemur, Vec3(0));
  Constraint::Weld rightHipConstraint (bodyMBody, Vec3(0, -halfBodyY, -0.25), rightFemur, Vec3(0));
  leftTibia.setDefaultAngle (Pi/10);
  /************** LeftLeg ***************/

  /************** Forces ***************/
  Force::MobilityDiscreteForce leftTibiaTorque(forces, leftTibia);
  Force::MobilityDiscreteForce rightTibiaTorque(forces, rightTibia);
  Force::MobilityDiscreteForce leftFemurTorque(forces, leftFemur);
  Force::MobilityDiscreteForce rightFemurTorque(forces, rightFemur);
  Force::MobilityDiscreteForce leftAnkleTorque(forces, leftAnklePin);
  Force::MobilityDiscreteForce rightAnkleTorque(forces, rightAnklePin);

  Force::MobilityLinearStop leftTibiaStop(forces, leftTibia, MobilizerQIndex(0), 0.2, 50, -Pi/3, Pi/3);
  Force::MobilityLinearStop rightTibiaStop(forces, rightTibia, MobilizerQIndex(0), 0.2, 50, -Pi/3, Pi/3);
  Force::MobilityLinearStop leftFemurStop(forces, leftFemur, MobilizerQIndex(0), 2, 5, -Pi/4, Pi/4);
  Force::MobilityLinearStop rightFemurStop(forces, rightFemur, MobilizerQIndex(0), 2, 5, -Pi/4, Pi/4);
  Force::MobilityLinearStop leftAnkleStop(forces, leftAnklePin, MobilizerQIndex(0), 2, 50, -Pi/4, Pi/4);
  Force::MobilityLinearStop rightAnkleStop(forces, rightAnklePin, MobilizerQIndex(0), 2, 50, -Pi/4, Pi/4);
  /************** Forces ***************/

#ifdef VIS_ON
  Visualizer viz(system);
  viz.setShowSimTime (true);
  viz.setShowFrameRate (true);
  viz.setMode(Visualizer::RealTime);
  viz.setDesiredBufferLengthInSec(1);
  viz.setDesiredFrameRate(30);
  matter.setShowDefaultGeometry(false);
  Visualizer::InputSilo* silo = new Visualizer::InputSilo();
  viz.addInputListener(silo);
  Array_<std::pair<String,int> > runMenuItems;
  runMenuItems.push_back(std::make_pair("Go", GoItem));
  runMenuItems.push_back(std::make_pair("Replay", ReplayItem));
  runMenuItems.push_back(std::make_pair("Quit", QuitItem));
  viz.addMenu("Run", RunMenuId, runMenuItems);
  system.addEventReporter(new Visualizer::Reporter(viz, 1.0/30));
#endif

  system.realizeTopology();

  State defaultState = system.getDefaultState();
  system.project (defaultState);
#ifdef VIS_ON
  viz.report(defaultState);
  saveEm.push_back(defaultState);
#endif
  RungeKuttaMersonIntegrator integ(system);
  integ.setAccuracy(0.05);
  integ.setConstraintTolerance(0.01);
  integ.setAllowInterpolation(false);
  integ.initialize(defaultState);
  unsigned stepNum = 0;
  short stateMachine = 0;
  float currentXPos = 0;
  float timeOfPrevSwitch = 0;
  bool locked = true;
  bool firstStep = true;
  while (integ.getTime() < simTime) {
    try {
      State& state = integ.updAdvancedState();
      system.realize (state, Stage::Velocity);
#ifdef VIS_ON
      saveEm.push_back(state);
#endif
      int menu, item;
      if (controller) {
        /****************************************************** Controller ******************************************************/
        bool leftFootOnFloor = false;
        bool rightFootOnFloor = false;
        if (leftAnklePin.getBodyOriginLocation(state)[1] < (halfFootBodyY + 0.031)) {
          leftFootOnFloor = true;
        }
        if (rightAnklePin.getBodyOriginLocation(state)[1] < (halfFootBodyY + 0.031)) {
          rightFootOnFloor = true;
        }

        if (locked == true && integ.getTime() > 2) {
          locked = false;
        }

        if (!locked) {
          if (stateMachine == 0) {
            if (((leftFemur.getRate (state) < stableTolerance) && leftTibia.getRate(state) < stableTolerance 
                  && leftAnklePin.getRate(state) < stableTolerance) && ((rightFemur.getRate (state) < stableTolerance) 
                  && rightTibia.getRate(state) < stableTolerance && rightAnklePin.getRate(state) < stableTolerance) 
                && bodyMBody.getBodyOriginVelocity(state).sum() < stableTolerance) {
              if (leftAnklePin.getBodyOriginLocation(state)[0] > rightAnklePin.getBodyOriginLocation(state)[0]) {
                stateMachine = 2;
                rightFootConstraint.disable (state);
              }
              else {
                stateMachine = 1;
                leftFootConstraint.disable (state);
              }
              system.realize (state, Stage::Velocity);
              currentXPos = (footMobodLeft.getBodyOriginLocation(state)[0] + footMobodRight.getBodyOriginLocation(state)[0])/2  + 0.8;
            }
          }
          else if (stateMachine == 1) {
            if (leftAnklePin.getBodyOriginLocation(state)[1] < (halfFootBodyY + 0.001) && leftAnklePin.getBodyOriginLocation(state)[0] > rightAnklePin.getBodyOriginLocation(state)[0] + (firstStep ? 0.01 : 0.04)) {
              if (firstStep) {
                firstStep = false;
              }
              stateMachine = 0;
              leftFootConstraint.setDefaultFrameOnBody2 
                (Transform(Vec3(leftAnklePin.getBodyOriginLocation(state)[0], 0, leftAnklePin.getBodyOriginLocation(state)[2])));
              leftFootConstraint.enable (state);
              system.project(state);
              integ.stepBy(MaxStepSize);
              state = integ.updAdvancedState();
              system.realize (state, Stage::Velocity);
#ifdef VIS_ON
              viz.report(state);
              saveEm.push_back(state);
#endif
            }
          }
          else if (stateMachine == 2) {
            if (rightAnklePin.getBodyOriginLocation(state)[1] < (halfFootBodyY + 0.001) && rightAnklePin.getBodyOriginLocation(state)[0] > leftAnklePin.getBodyOriginLocation(state)[0] + (firstStep ? 0.01 : 0.04)) {
              if (firstStep) {
                firstStep = false;
              }
              stateMachine = 0;
              rightFootConstraint.setDefaultFrameOnBody2 
                (Transform(Vec3(rightAnklePin.getBodyOriginLocation(state)[0], 0, rightAnklePin.getBodyOriginLocation(state)[2])));
              rightFootConstraint.enable (state);
              system.project(state);
              integ.stepBy(MaxStepSize);
              state = integ.updAdvancedState();
              system.realize (state, Stage::Velocity);
#ifdef VIS_ON
              viz.report(state);
              saveEm.push_back(state);
#endif
            }
          }
        }

        /* Applied Force Vector */
        mat fVecLeft;
        mat fVecRight;
        mat torquesRight;
        mat torquesLeft;
        Vec3 pos = bodyMBody.getBodyOriginLocation (state);
        Vec3 vel = bodyMBody.getBodyOriginVelocity (state);
        if (pos[1] < (tibiaLength + femurLength + halfFootBodyY + halfBodyY)/3) {
          // cout << "-2";
          return -2;
        }
        if (stateMachine == 0) {
          double fX = -k1* (-currentXPos + pos[0]) - lambda1 * (-speed + vel[0]);
          double fY = -k2 * (pos[1] - (tibiaLength + femurLength) + halfBodyY + halfFootBodyY + standOffset) -lambda2 * vel[1];
          double fPhiLeft = leftFemur.getAngle (state) * bodyStraightK + leftFemur.getRate (state) * bodyStraightLambda;
          double fPhiRight = rightFemur.getAngle (state) * bodyStraightK + rightFemur.getRate (state) * bodyStraightLambda;

          fVecLeft << fX << endr << fY << endr << fPhiLeft << endr;
          fVecRight << fX << endr << fY << endr << fPhiRight << endr;
          /* Left Leg constants */
          double L2sin_L = femurLength * sin (-leftTibia.getAngle (state) - (leftAnklePin.getAngle (state))); //L2sin(theta_k-theta_a)
          double L2cos_L = femurLength * cos (-leftTibia.getAngle (state) - (leftAnklePin.getAngle (state))); //L2cos(theta_k-theta_a)
          double L1sin_L = tibiaLength * sin (leftAnklePin.getAngle(state)); //L1cos(theta_a)
          double L1cos_L = tibiaLength * cos (leftAnklePin.getAngle(state)); //L1sin(theta_a)

          mat jacLeft;
          jacLeft << L1cos_L + L2cos_L << L1sin_L - L2sin_L << 1 << endr
            << L2cos_L << -L2sin_L << 1 << endr
            << 0 << 0 << 1 << endr;

          torquesLeft = jacLeft * fVecLeft;
          /* Left Leg constants */

          /* Right Leg constants */
          double L2sin_R = femurLength * sin (-rightTibia.getAngle (state) - (rightAnklePin.getAngle (state))); //L2sin(theta_k-theta_a)
          double L2cos_R = femurLength * cos (-rightTibia.getAngle (state) - (rightAnklePin.getAngle (state))); //L2cos(theta_k-theta_a)
          double L1sin_R = tibiaLength * sin (rightAnklePin.getAngle(state)); //L1cos(theta_a)
          double L1cos_R = tibiaLength * cos (rightAnklePin.getAngle(state)); //L1sin(theta_a)

          mat jacRight;
          jacRight << L1cos_R + L2cos_R << L1sin_R - L2sin_R << 1 << endr
            << L2cos_R << -L2sin_R << 1 << endr
            << 0 << 0 << 1 << endr;

          torquesRight = jacRight * fVecRight;
          /* Right Leg constants */
        }
        else if (stateMachine == 1) {
          double fX   = 2*(-k1* (-currentXPos + pos[0]) - lambda1 * (-speed + vel[0]));
          double fY = -2*k2 * (pos[1] - (tibiaLength + femurLength) + halfBodyY + halfFootBodyY + stepOffset) -1*lambda2 * vel[1];
          double fPhiRight = 2*(rightFemur.getAngle (state) * bodyStraightK + rightFemur.getRate (state) * bodyStraightLambda);

          fVecRight << fX << endr << fY << endr << fPhiRight << endr;
          /* Right Leg constants */
          double L2sin_R = femurLength * sin (-rightTibia.getAngle (state) - (rightAnklePin.getAngle (state))); //L2sin(theta_k-theta_a)
          double L2cos_R = femurLength * cos (-rightTibia.getAngle (state) - (rightAnklePin.getAngle (state))); //L2cos(theta_k-theta_a)
          double L1sin_R = tibiaLength * sin (rightAnklePin.getAngle(state)); //L1cos(theta_a)
          double L1cos_R = tibiaLength * cos (rightAnklePin.getAngle(state)); //L1sin(theta_a)
          /* Right Leg constants */

          mat jacRight;
          jacRight << L1cos_R + L2cos_R << L1sin_R - L2sin_R << 1 << endr
            << L2cos_R << -L2sin_R << 1 << endr
            << 0 << 0 << 1 << endr;

          torquesRight = jacRight * fVecRight;

          torquesLeft << 0 << endr << 0 << endr << (Pi/5 + leftFemur.getAngle(state))*stepK << endr;
        }
        else if (stateMachine == 2) {
          double fX   = 2*(-k1* (-currentXPos + pos[0]) - lambda1 * (-speed + vel[0]));
          double fY = -2*k2 * (pos[1] - (tibiaLength + femurLength) + halfBodyY + halfFootBodyY + stepOffset) -1*lambda2 * vel[1];
          double fPhiLeft = 2*(leftFemur.getAngle (state) * bodyStraightK + leftFemur.getRate (state) * bodyStraightLambda);

          fVecLeft << fX << endr << fY << endr << fPhiLeft << endr;
          /* Left Leg constants */
          double L2sin_R = femurLength * sin (-leftTibia.getAngle (state) - (leftAnklePin.getAngle (state))); //L2sin(theta_k-theta_a)
          double L2cos_R = femurLength * cos (-leftTibia.getAngle (state) - (leftAnklePin.getAngle (state))); //L2cos(theta_k-theta_a)
          double L1sin_R = tibiaLength * sin (leftAnklePin.getAngle(state)); //L1cos(theta_a)
          double L1cos_R = tibiaLength * cos (leftAnklePin.getAngle(state)); //L1sin(theta_a)
          /* Left Leg constants */

          mat jacLeft;
          jacLeft << L1cos_R + L2cos_R << L1sin_R - L2sin_R << 1 << endr
            << L2cos_R << -L2sin_R << 1 << endr
            << 0 << 0 << 1 << endr;

          torquesLeft = jacLeft * fVecLeft;

          torquesRight << 0 << endr << 0 << endr << (Pi/5 + rightFemur.getAngle(state))*stepK << endr;
        }

        /* Apply Torques */
        if (leftFootOnFloor || stateMachine == 1) {
          leftAnkleTorque.setMobilityForce (state, -torquesLeft (0, 0));
          leftTibiaTorque.setMobilityForce (state, -torquesLeft (1, 0));
          leftFemurTorque.setMobilityForce (state, -torquesLeft (2, 0));
        }
        else {
          leftAnkleTorque.setMobilityForce (state, 0);
          leftTibiaTorque.setMobilityForce (state, 0);
          leftFemurTorque.setMobilityForce (state, 0);
        }

        if (rightFootOnFloor || stateMachine == 2) {
          rightAnkleTorque.setMobilityForce (state, -torquesRight (0, 0));
          rightTibiaTorque.setMobilityForce (state, -torquesRight (1, 0));
          rightFemurTorque.setMobilityForce (state, -torquesRight (2, 0));
        }
        else {
          rightAnkleTorque.setMobilityForce (state, 0);
          rightTibiaTorque.setMobilityForce (state, 0);
          rightFemurTorque.setMobilityForce (state, 0);
        }
        /* Apply Torques */
        /****************************************************** Controller ******************************************************/
      }
      if (!leftFootConstraint.isDisabled(state)) {
        //system.realize (state, Stage::Acceleration);
        //double a = leftFootConstraint.getConstrainedBodyForcesAsVector (state)[0][1][1];
      }

#ifdef VIS_ON
      if (stepNum % DrawEveryN == 0) {
        viz.report(state);
      }
#endif
      integ.stepBy(MaxStepSize);
      ++stepNum;
      if (integ.getTime() >= simTime) {
        float finalLeftFootPos = footMobodLeft.getBodyOriginLocation(state)[0];
        float finalRightFootPos = footMobodRight.getBodyOriginLocation(state)[0];
        float fitness = ((finalRightFootPos > finalLeftFootPos) ? finalLeftFootPos : finalRightFootPos);
#ifdef VIS_ON
        cout << fitness << endl;
#endif
        // fitness = fitness / 1.;
        fitness = fitness / (tibiaLength + femurLength);
        cout << fitness;
        std::flush(std::cout);
      }
    }
    catch (exception& e) {
      cout << "-1";
      cerr << e.what() << endl;
      std::flush(std::cout);
      return -1;
    }
  }
  // Add as slider to control playback speed.
#ifdef VIS_ON
  viz.addSlider("Speed", 1, 0, 4, 1);
  viz.setMode(Visualizer::PassThrough);

  silo->clear(); // forget earlier input
  double animationSpeed = 1; // will change if slider moves
  while(true) {

    int menuId, item;
    silo->waitForMenuPick(menuId, item);

    if (menuId != RunMenuId) {
      cout << "\aUse the Run menu!\n";
      continue;
    }

    if (item == QuitItem)
      break;
    if (item != ReplayItem) {
      cout << "\aHuh? Try again.\n";
      continue;
    }

    for (double i=0; i < (int)saveEm.size(); i += animationSpeed ) {
      int slider; Real newValue;
      if (silo->takeSliderMove(slider,newValue)) {
        animationSpeed = newValue;
      }
      viz.report(saveEm[(int)i]);
    }
  }
#endif
  return 0;

}
