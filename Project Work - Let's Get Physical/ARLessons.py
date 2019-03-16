using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Experimental.XR;
using UnityEngine.XR.ARFoundation;
using TMPro;
using UnityEngine.EventSystems;

public class ARLesson : MonoBehaviour
{

    // Variables related to Unity objects
    [SerializeField] private TMP_Text stateText;
    [SerializeField] private TMP_Text planesText;
    [SerializeField] private ARPlaneManager aRPlaneManager;
    [SerializeField] private ARPointCloudManager aRPointCloudManager;
    [SerializeField] private GameObject m_RobotPrefab;
    [SerializeField] private ARSessionOrigin m_SessionOrigin;
    [SerializeField] private Light m_Light;
    [SerializeField] private Image m_ImageLighting;
    [SerializeField] private GameObject m_BallPrefab;

    // Variables for this class
    private List<ARPlane> activePlanes = new List<ARPlane>();
    private List<Vector3> activePoints = new List<Vector3>();

    // To handle raycast hits
    static List<ARRaycastHit> s_Hits = new List<ARRaycastHit>();

    // The object instantiated as a result of a successful raycast intersection with a plane.
    public GameObject spawnedObject { get; private set; }

    // The estimated brightness of the physical environment, if available.
    public float? brightness { get; private set; }
    // The estimated color temperature of the physical environment, if available.
    public float? colorTemperature { get; private set; }
    // The estimated color correction value of the physical environment, if available.
    public Color? colorCorrection { get; private set; }


    // Start is called before the first frame update
    void Start()
    {
        // Update texts at start
        UpdateTextPlanes();

        // Add callbacks
        ARSubsystemManager.systemStateChanged += OnSystemStateChanged;
        aRPlaneManager.planeAdded += OnPlaneAdded;
        aRPlaneManager.planeRemoved += OnPlaneRemoved;
        aRPlaneManager.planeUpdated += OnPlaneUpdated;
        aRPointCloudManager.pointCloudUpdated += OnPointCloudUpdated;
        ARSubsystemManager.cameraFrameReceived += OnCameraFrameReceived;
    }

    // Update is called once per frame
    void Update()
    {
        // Update number of planes and cloud points text
        UpdateTextPlanes();

        // Handle screen touches.
        if (Input.touchCount > 0 && Input.GetTouch(0).phase == TouchPhase.Began)
        {
            Touch touch = Input.GetTouch(0);

            if (!EventSystem.current.IsPointerOverGameObject(touch.fingerId))
            {
                if (m_SessionOrigin.Raycast(touch.position, s_Hits, TrackableType.PlaneWithinPolygon))
                {
                    // Raycast hits are sorted by distance, so the first one will be the closest hit.
                    var hitPose = s_Hits[0].pose;
                    if (spawnedObject == null)
                    {
                        spawnedObject = Instantiate<GameObject>(m_RobotPrefab);
                    }
                    // Whether it is just instatiated or not, move it at touch position 
                    spawnedObject.transform.position = hitPose.position;
                    Rigidbody rb = spawnedObject.GetComponent<Rigidbody>();
                    rb.isKinematic = true;
                    rb.angularVelocity = new Vector3(0, 0, 0);
                    rb.velocity = new Vector3(0, 0, 0);
                }
            }
        }
    }

    // Callbacks
    private void OnSystemStateChanged(ARSystemStateChangedEventArgs obj)
    {
        stateText.text = obj.state.ToString();
    }

    private void OnPlaneAdded(ARPlaneAddedEventArgs args)
    {
        if (!activePlanes.Contains(args.plane))
        {
            activePlanes.Add(args.plane);
        }
    }

    private void OnPlaneRemoved(ARPlaneRemovedEventArgs args)
    {
        if (activePlanes.Contains(args.plane))
        {
            activePlanes.Remove(args.plane);
        }
    }

    private void OnPlaneUpdated(ARPlaneUpdatedEventArgs args)
    {
        /* TODO: Code for when two planes merge.
        Tried a lot of things but I could not find how to check which planes merged. 
        Here are some code snippets that I tried but did not work:
        1.  if (args.plane.trackingState == UnityEngine.Experimental.XR.TrackingState.Unavailable)
            {
                activePlanes.Remove(args.plane);
            }
        2.  foreach (ARPlane plane in activePlanes)
            {
                if (plane.trackingState == UnityEngine.Experimental.XR.TrackingState.Unavailable)
                {
                    activePlanes.Remove(plane);
                }
            }
        */
    }

    private void OnPointCloudUpdated(ARPointCloudUpdatedEventArgs args)
    {
        args.pointCloud.GetPoints(activePoints);
    }

    private void OnCameraFrameReceived(ARCameraFrameEventArgs args)
    {
        if (args.lightEstimation.averageBrightness.HasValue)
        {
            brightness = args.lightEstimation.averageBrightness.Value;
            m_Light.intensity = brightness.Value;
        }

        if (args.lightEstimation.averageColorTemperature.HasValue)
        {
            colorTemperature = args.lightEstimation.averageColorTemperature.Value;
            m_Light.colorTemperature = colorTemperature.Value;
        }

        if (args.lightEstimation.colorCorrection.HasValue)
        {
            colorCorrection = args.lightEstimation.colorCorrection.Value;
            m_Light.color = colorCorrection.Value;
            m_ImageLighting.color = colorCorrection.Value;
        }
    }

    // Function to update the Plane Text
    private void UpdateTextPlanes()
    {
        planesText.text = $"% planes: {activePlanes.Count}\n % points: {activePoints.Count}";
    }

    // Shoot a Ball
    public void ShootBall()
    {
        GameObject newBall = Instantiate<GameObject>(m_BallPrefab);
        newBall.transform.position = Camera.main.transform.position; // Make sure your camera object is tagged as "Main Camera" in the Unity editor
        Rigidbody rb = newBall.GetComponent<Rigidbody>();
        rb.AddForce(5000 * Camera.main.transform.forward);
    }
}