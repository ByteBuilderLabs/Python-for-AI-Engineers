$strategies = [ordered]@{ unpinned = "requirements.txt"; compat = "requirements-compat.txt"; locked = "uv.lock" }
$dates = [ordered]@{ old = "2026-10-06T00:00:00Z"; new = "2026-10-27T00:00:00Z" }
mkdir out -Force | Out-Null

foreach ($s in $strategies.Keys) {
    foreach ($d in $dates.Keys) {
        $build = "$s-$d"
        docker build --no-cache -q -t $build --build-arg REQS=$($strategies[$s]) --build-arg CUTOFF=$($dates[$d]) .
        if ($LASTEXITCODE -ne 0) { throw "Build failed: $build" }
        docker run --rm -e OPENAI_API_KEY -e BUILD=$build -v "${PWD}\out:/out" $build
    }
}