export function useGeolocation() {
  function getPositionWithTimeout(timeoutMs = 10000) {
    return new Promise((resolve, reject) => {
      let settled = false
      const timer = setTimeout(() => {
        if (!settled) { settled = true; reject(new Error('GPS Timeout')) }
      }, timeoutMs)

      navigator.geolocation.getCurrentPosition(
        pos => { if (!settled) { settled = true; clearTimeout(timer); resolve(pos) } },
        err => { if (!settled) { settled = true; clearTimeout(timer); reject(err) } },
        { enableHighAccuracy: true, timeout: timeoutMs, maximumAge: 0 }
      )
    })
  }

  return { getPositionWithTimeout }
}
